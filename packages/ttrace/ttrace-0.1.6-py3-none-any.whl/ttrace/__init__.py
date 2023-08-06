#!/usr/bin/env python3

"""Visualize strace output
"""

import os
import re
import signal
import sys
from argparse import ArgumentParser, Namespace
from ast import literal_eval
from asyncio import StreamReader, create_subprocess_exec, gather, run
from asyncio.subprocess import PIPE
from collections.abc import (
    AsyncIterable,
    Iterator,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Any, ClassVar, NoReturn, Protocol, TextIO, Type, TypeVar

import aiofiles

from .utils.treestuff import attributed_tree, colored, get_node, insert

PPID = r"\d*"
PTIME = r"\d{10}\.\d{6}"
PFNAME = r"([a-z0-9_]*|\?*)"
PHEX = r"0x[0-9a-f]*"
PCOMMENT = r"\/\*\s(.*)\s\*\/"
PRESULT = rf"(\?|-?\d*|{PHEX})( [A-Z]*)?( \(.*\))?( {PCOMMENT})?"
PPATH = r".*"
PFLAGS = r"[A-Z_\|]*"
PCONST = r"([A-Z_]*|\d*)"
PPERMISSION = r"0[0-7]{3}|000"
PANYTHING = r".*"

ALL_COMMANDS = set(
    "exited "
    "execve openat vfork clone clone3 "
    "getrusage fstatfs dup getegid rt_sigaction rmdir close rt_sigprocmask "
    "getrandom pipe2 write getcwd lseek munmap getppid unlinkat clock_nanosleep "
    "mprotect getpid readlink getpgrp setresuid sched_getaffinity fcntl umask "
    "gettid wait4 getuid rt_sigreturn sysinfo getdents64 sigaltstack "
    "geteuid chmod exit_group set_tid_address setresgid brk uname access "
    "fsetxattr mkdir pread64 set_robust_list rseq faccessat2 ioctl getgid "
    "renameat2 newfstatat tgkill mmap statx unlink splice prlimit64 dup2 "
    "getgroups kill arch_prctl read statfs rename chdir symlinkat fadvise64".split()
)


def parse_args(args: Sequence[str] | None = None) -> tuple[Namespace, Sequence[str]]:
    """Returns parsed arguments until the first
    >>> parse_args(["-v", "--grep", "abc", "foo", "-v", "bar"])
    (Namespace(verbose=True, record=None, grep='abc'), ['foo', '-v', 'bar'])
    """

    class MyArgumentParser(ArgumentParser):
        """Argument parser which not exits on error but raises an exception"""

        def error(self, message: str) -> NoReturn:
            """Just raises an error we can catch"""
            raise RuntimeError(message)

    parser = MyArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--record", "-r", type=Path)
    parser.add_argument("--grep", "-g", type=str)

    all_args = args or sys.argv[1:]
    for split_at in (i for i, e in reversed(list(enumerate(all_args))) if not e.startswith("-")):
        try:
            return parser.parse_args(all_args[:split_at]), all_args[split_at:]
        except RuntimeError as exc:
            if any(not e.startswith("-") for e in all_args[:split_at]):
                continue
            parser.print_help(sys.stderr)
            print(exc, file=sys.stderr)
            raise SystemExit(-1) from exc

    parser.print_help(sys.stderr)
    print("No command provided", file=sys.stderr)
    raise SystemExit(-1)


@dataclass
class StraceType:
    """A full strace logline, consisting of the PID, a unix timestamp (us),
    the syscall command name, the (unparsed) arguments and its result
    >>> parse(StraceType, "727862 1676908243.245515 foo(-1) = 42 (the answer) /* to everything */")
    strace<pid=727862, t=1676908243.245515, cmd=foo, res_nr=42, comment='to everything'>
    >>> parse(StraceType, "500918 1677690227.029671 +++ exited with 23 +++")
    strace<pid=500918, t=1677690227.029671, cmd=exited, res_nr=23, comment=None>
    """

    pid: int
    timestamp: str
    fname: str
    args: str
    result: str
    result_nr: int | None
    PATTERN: ClassVar[str] = (
        rf"^({PPID})\s({PTIME})\s("
        rf"(({PFNAME})\(({PANYTHING})\)\s=\s({PRESULT}))"
        rf"|(\+\+\+ (exited) with (-?\d*) \+\+\+)"
        rf")$"
    )

    def __init__(self, args: tuple[str, ...]) -> None:
        self.pid = int(args[0])
        assert self.pid
        self.timestamp = args[1]
        self.fname = args[4] or args[14]
        assert self.fname
        self.args = args[6]
        self.result = args[7] or args[13]
        assert self.result
        result_nr_str = args[8] or args[15]
        assert result_nr_str is not None
        self.result_nr = int(result_nr_str) if result_nr_str != "?" else None
        self.comment = args[12]

    def __repr__(self) -> str:
        return (
            f"strace<pid={self.pid}"
            f", t={self.timestamp}"
            f", cmd={self.fname}"
            f", res_nr={self.result_nr}"
            f", comment={self.comment!r}>"
        )


@dataclass
class UnfinishedType:
    """Recognizes an `unfinished` strace element and stores PID (there is only
    one continuation per PID) and the part of the line needed to stitch it
    together later.
    >>> parse(UnfinishedType, "727862 1676908243.245515 wait4(-1,  <unfinished ...>")
    unfinished<pid=727862>
    >>> parse(UnfinishedType, "160833 1677921270.753070 ???( <unfinished ...>")
    unfinished<pid=160833>
    """

    line: str
    pid: int

    PATTERN: ClassVar[
        str
    ] = rf"^(({PPID})\s{PTIME}\s{PFNAME}\({PANYTHING})\s<unfinished\s\.\.\.>{PANYTHING}$"

    def __init__(self, args: tuple[str, ...]) -> None:
        self.line = args[0]
        self.pid = int(args[1])

    def __repr__(self) -> str:
        return f"unfinished<pid={self.pid}>"


@dataclass
class ResumedType:
    """Recognizes a `resumed` strace element and stores PID and the part of the
    line needed to stitch it to the previous `unfinished` element.
    >>> parse(ResumedType, "727862 1676908243.255635 <... wait4 resumed>blabla) = 727863")
    resumed<pid=727862>
    """

    pid: int
    line: str
    PATTERN: ClassVar[str] = rf"^({PPID})\s{PTIME}\s<\.\.\. {PFNAME} resumed>({PANYTHING})$"

    def __init__(self, args: tuple[str, ...]) -> None:
        self.pid = int(args[0])
        self.line = args[2]

    def __repr__(self) -> str:
        return f"resumed<pid={self.pid}>"


@dataclass
class ExecveType:
    """Content of an execve() call, including the path to the executable,
    the actual command with its arguments and the environment variables
    used for this command
    >>> parse(ExecveType, '"/bin/foo", ["foo", "-v"], ["FOO=bar"]')
    execve<exe='/bin/foo', cmd=['foo -v']>
    """

    executable: str
    command: str
    environment: str
    PATTERN: ClassVar[str] = rf'^"({PPATH})", \[({PANYTHING})\], \[({PANYTHING})\]$'

    def __init__(self, args: tuple[str, ...]) -> None:
        self.executable = args[0]
        self.command = literal_eval(args[1])
        self.environment = args[2]

    def __repr__(self) -> str:
        return f"execve<exe={self.executable!r}, cmd=[{' '.join(self.command)!r}]>"


@dataclass
class OpenatType:
    """Content of an openat() call, including the path to the opened file and
    the flags being used
    >>> parse(OpenatType, 'AT_FDCWD, "/usr/bin/print", O_RDONLY|O_CLOEXEC')
    openat<path='/usr/bin/print'>
    """

    position: str
    path: str
    flags: str
    PATTERN: ClassVar[str] = rf'^([A-Z_]*|\d*),\s"({PANYTHING})", ({PFLAGS})(, ({PPERMISSION}))?$'

    def __init__(self, args: tuple[str, ...]) -> None:
        self.position = args[0]
        self.path = args[1]
        self.flags = args[2]

    def __repr__(self) -> str:
        return f"openat<path={self.path!r}>"


@dataclass
class VforkType:
    """Content of an vfork() call
    >>> parse(VforkType, '')
    vfork<>
    """

    PATTERN: ClassVar[str] = r"^$"

    def __init__(self, _args: tuple[str, ...]) -> None:
        ...

    def __repr__(self) -> str:
        return "vfork<>"


@dataclass
class CloneType:
    """Content of an clone() call
    >>> parse(CloneType, 'child_stack=NULL, flags=SIGCHLD, child_tidptr=0x123')
    clone<child_stack='NULL', flags=['SIGCHLD'], child_tidptr='0x123'>
    """

    child_stack: str
    flags: Sequence[str]
    child_tidptr: str

    PATTERN: ClassVar[str] = (
        rf"^child_stack=(.*), flags=({PFLAGS})" rf"(, child_tidptr=(.*))?" rf"(, tls=({PHEX}))?$"
    )

    def __init__(self, args: tuple[str, ...]) -> None:
        self.child_stack = args[0]
        self.flags = args[1].split("|")
        self.child_tidptr = args[3]

    def __repr__(self) -> str:
        return (
            f"clone<child_stack={self.child_stack!r}"
            f", flags={self.flags!r}, child_tidptr={self.child_tidptr!r}>"
        )


@dataclass
class Clone3Type:
    """Content of an clone3() call
    >> parse(Clone3Type, '{flags=FOO, exit_signal=SIGCHLD, stack=0x123, stack_size=0x90}, 88')
    clone3<flags=['FOO'], parent_tid_comment=None>
    >>> parse(Clone3Type,
    ...     '{flags=FOO|BAR, child_tid=0x123, parent_tid=0x345'
    ...     ', exit_signal=0, stack=0x234, stack_size=0x54, tls=0x2345}'
    ...     ' => {parent_tid=[1869 /* 1803473 in strace\\'s PID NS */]}, 88')
    clone3<flags=['FOO', 'BAR'], parent_tid_comment="1803473 in strace's PID NS">
    """

    flags: Sequence[str]
    parent_tid_comment: str
    PATTERN: ClassVar[str] = (
        rf"^\{{flags=({PFLAGS})(, child_tid={PHEX})?(, parent_tid={PHEX})?"
        rf"(, exit_signal={PCONST})?, stack={PHEX}, stack_size={PHEX}(, tls={PHEX})?\}}"
        rf"( => \{{parent_tid=\[(\d*)( {PCOMMENT})?\]\}})?, \d*$"
    )

    def __init__(self, args: tuple[str, ...]) -> None:
        self.flags = args[0].split("|")
        self.parent_tid_comment = args[9]

    def __repr__(self) -> str:
        return f"clone3<flags={self.flags}, parent_tid_comment={self.parent_tid_comment!r}>"


class ParsableBase(Protocol):  # pylint: disable=too-few-public-methods
    """Needed only to be able to access PATTERN inside parse(), see
    https://stackoverflow.com/questions/75507292"""

    PATTERN: ClassVar[str]

    def __init__(self, args: tuple[str, ...]) -> None:
        ...


Parsable = TypeVar("Parsable", bound=ParsableBase)


def parse(
    result_type: Type[Parsable], line: str, raise_on_mismatch: bool = True
) -> Parsable | None:
    """Returns an element of given class from parsed line
    >>> parse(StraceType, '012345 1234567890.123456 abc(a, b, c) = 1')
    strace<pid=12345, t=1234567890.123456, cmd=abc, res_nr=1, comment=None>
    """
    if (match := re.match(result_type.PATTERN, line)) is None:
        if raise_on_mismatch:
            raise RuntimeError(
                f"Could not parse a {result_type.__name__} from {line!r} with pattern"
                f" {result_type.PATTERN}"
            )
        return None
    return result_type(match.groups())


async def sanatized_strace_lines(filename: Path) -> AsyncIterable[tuple[str, StraceType]]:
    """Returns fully usable strace entries"""
    # pylint: disable=too-many-branches

    resume_state: MutableMapping[int, UnfinishedType] = {}
    pid_gen = {"clone", "clone3", "vfork"}
    line_stack_open: MutableSequence[tuple[str, StraceType]] = []
    line_stack: MutableSequence[tuple[str, StraceType]] = []

    try:
        async with aiofiles.open(filename) as afp:
            # https://github.com/Tinche/aiofiles/issues/105
            async for line in afp:  # type: ignore[attr-defined]
                if strace := parse(StraceType, line, raise_on_mismatch=False):
                    if "<unfinished ...>" in line:
                        print(line)
                        print(StraceType.PATTERN)
                        raise SystemExit(1)
                    assert " resumed>" not in line
                    if strace.fname == "exited" and strace.pid in resume_state:
                        del resume_state[strace.pid]

                    if resume_state:
                        (line_stack_open if strace.fname in pid_gen else line_stack).append(
                            (line.rstrip(), strace)
                        )
                    else:
                        yield line.rstrip(), strace
                    continue

                if unfinished := parse(UnfinishedType, line, raise_on_mismatch=False):
                    assert unfinished.pid not in resume_state
                    resume_state[unfinished.pid] = unfinished
                    continue

                if resumed := parse(ResumedType, line, raise_on_mismatch=False):
                    if resumed.pid not in resume_state:
                        raise RuntimeError(
                            f"'resumed' without corresponding 'unfinished' found: {line}"
                        )
                    continued_line = resume_state[resumed.pid].line + resumed.line
                    del resume_state[resumed.pid]

                    if not (continued_strace := parse(StraceType, continued_line)):
                        raise RuntimeError()

                    (line_stack_open if continued_strace.fname in pid_gen else line_stack).append(
                        (continued_line.rstrip(), continued_strace)
                    )

                    if not resume_state:
                        for element in line_stack_open:
                            yield element
                        line_stack_open.clear()
                        for element in line_stack:
                            yield element
                        line_stack.clear()
                    continue

                if any(s in line for s in ("+++ killed ", " --- ")):
                    continue

                # Should raise
                parse(StraceType, line)

    finally:
        assert not resume_state


async def read_strace(filename: Path, args: Namespace) -> None:
    """Reads strace log from a file (e.g. a named pipe) and handles all entries"""
    # this will become a generator similar to sanatized_strace_lines but for PID tracking
    # until then we accept 'too-many-branches' and 'too-many-statements'
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    # maps PIDs to a fork type - maybe we can get rid of this in the future in favor of `ptree`
    pid_path: MutableMapping[str | int, Sequence[int]] = {}
    ptree: MutableMapping[str | int, Any] = {}

    try:
        async for line, strace in sanatized_strace_lines(filename):
            if strace.result_nr is None:
                assert strace.fname in {"vfork", "clone", "clone3"}
                continue

            if args.grep and re.findall(args.grep, line):
                print(line)

            assert strace.fname in ALL_COMMANDS, f"{strace.fname}"

            if len(pid_path) == 0:
                # this is the first call. make sure we register the PID even though we have no
                # fork type yet
                assert strace.fname == "execve"
                pid_path[strace.pid] = [strace.pid]
                insert(
                    ptree,
                    path=[],
                    name=strace.pid,
                    # display_name=execve.fname[0],
                    attrs={
                        "tags": [],
                    },
                )

            if strace.pid not in pid_path:
                print(">>>", line)
                print(colored(f"{strace}", "yellow_bold"))
                assert strace.pid in pid_path, f"{strace.pid} not in `pid_path`"

            if strace.fname == "execve":
                if strace.result_nr >= 0:
                    execve = parse(ExecveType, strace.args)
                    assert execve
                    if args.verbose:
                        print(
                            colored(
                                f"{strace.pid}|execve |"
                                # f"execve |{'.'.join(pid_path[strace.pid][0])}.{strace.pid}|"
                                f"{strace.result}| {execve.command}",
                                "green_bold",
                            )
                        )
                    get_node(ptree, pid_path[strace.pid]).setdefault("__attrs__", {}).setdefault(
                        "tags", []
                    ).append(execve.command[0])

            elif strace.fname in {"vfork", "clone", "clone3"}:
                new_pid = int(strace.comment.split()[0]) if strace.comment else strace.result_nr
                assert new_pid not in pid_path
                pid_path[new_pid] = list(chain(pid_path[strace.pid], [new_pid]))

                if args.verbose:
                    if strace.fname == "vfork":
                        vfork = parse(VforkType, strace.args)
                        assert vfork
                        print(colored(f"{strace.pid}|vfork  |{strace.result_nr}|", "blue_bold"))

                    elif strace.fname == "clone":
                        clone = parse(CloneType, strace.args)
                        assert clone
                        print(colored(f"{strace.pid}|clone  |{strace.result_nr}|", "blue_bold"))

                    elif strace.fname == "clone3":
                        clone3 = parse(Clone3Type, strace.args)
                        assert clone3
                        print(colored(f"{strace.pid}|clone3 |{strace.result_nr}|", "blue_bold"))

                insert(
                    ptree,
                    path=pid_path[strace.pid],
                    name=new_pid,
                    ## display_name=execve.command[0],
                    attrs={
                        "tags": [strace.fname],
                    },
                )

            elif strace.fname == "openat":
                openat = parse(OpenatType, strace.args)
                assert openat
                if not strace.result.startswith("-1"):
                    if (
                        args.verbose
                        and openat.path not in {".", "/proc/filesystems", "/dev/null"}
                        and ".so" not in openat.path
                        and not any(openat.path.endswith(s) for s in (".h", ".c", ".o", ".a", ".s"))
                    ):
                        print(
                            colored(
                                f"{strace.pid}|openat |{strace.result}| {openat.path}", "blue_bold"
                            )
                        )
    finally:
        print(attributed_tree(ptree))


async def buffer_stream(stream: StreamReader, out_file: TextIO) -> None:
    """Records a given stream to a buffer line by line along with the source"""
    while line := (await stream.readline()).decode():
        out_file.write(line)


@contextmanager
def strace_output_path(path: Path | None = None) -> Iterator[Path]:
    """Wraps optional creation of named pipe and sanatizes @path argument"""
    result = path or Path("myfifo")
    result.unlink(missing_ok=True)
    try:
        if path is None:
            os.mkfifo(result, 0o600)
        yield result
    finally:
        if path is None:
            os.unlink(result)


async def main_invoke(cmd: Sequence[str], args: Namespace) -> None:
    """Runs a program using strace"""
    with strace_output_path(args.record) as output_file_path:
        full_cmd = (
            "strace",
            "--trace=fork,vfork,clone,clone3,execve,openat",
            "--decode-pids=pidns",
            "--timestamps=unix,us",
            "--follow-forks",
            "--columns=0",
            "--abbrev=none",
            "-s",
            "65536",
            "-o",
            f"{output_file_path}",
            *cmd,
        )

        if args.verbose:
            print(" ".join(full_cmd))

        process = await create_subprocess_exec(*full_cmd, stdout=PIPE, stderr=PIPE)

        assert process.stdout and process.stderr
        signal.signal(signal.SIGINT, lambda _sig, _frame: 0)

        await gather(
            *(
                awaitable
                for awaitable in (
                    buffer_stream(process.stdout, sys.stdout),
                    buffer_stream(process.stderr, sys.stderr),
                    None if args.record else read_strace(output_file_path, args),
                    process.wait(),
                )
                if awaitable
            )
        )
        raise SystemExit(process.returncode)


def main() -> int:
    """Main entrypoint"""
    args, command = parse_args()

    if command[0].endswith(".log"):
        run(read_strace(Path(command[0]), args))
    else:
        run(main_invoke(command, args))
    return 0


if __name__ == "__main__":
    main()
