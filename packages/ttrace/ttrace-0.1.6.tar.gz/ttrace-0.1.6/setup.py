# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttrace', 'ttrace.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=23.1.0,<24.0.0', 'treelib>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['ttrace = ttrace:main']}

setup_kwargs = {
    'name': 'ttrace',
    'version': '0.1.6',
    'description': 'Makes use of strace',
    'long_description': "# ttrace - strace as a tree\n\nUses `strace` to trace a program call and displays what's going on in a human\nfriendly manner.\n\n[Project page](https://projects.om-office.de/frans/ttrace)\n\n## Usage\n\nCurrently you just run\n\n```\nttrace.py <CMD>\n```\nas you would with `strace` but without any arguments to `ttrace` (`strace` will\nbe called with a bunch of arguments automatically).\n\nSee next section to see what's coming.\n\n## Intended interface\n\nThe following commands and outputs reflect the current development plan:\n\n```sh\nttrace <CMD|LOGFILE>\n```\nPrints annotated, pre-formatted and filtered output next to the process' original\n`stdout` and `stderr`.\n\n```sh\nttrace --attach <PID|NAME>\n```\nAttaches to the given process and displays all but `stdout` and `stderr` of the\nprocess of course.\n\n```sh\n<CMD> | ttrace [<OTHER-ARGS>]\n```\nSame as with `attach` but using pipe semantics (limited due to the mixing of\n`stderr` and `strace` output.\n\n\n```sh\nttrace --grep <PATTERN> <CMD>\n```\nApplies pattern to the original `strace` output and only outputs the matching\ncontent.\n\n```sh\nttrace --tree <CMD>\n```\nPopulates and displays a tree while the program is running.\n\n```sh\nttrace --hybrid <CMD>\n```\nNot sure yet - plan is to have `ncurses` based split views for optionally any\nof the following elements:\n\n* tree output\n* combined `stdout` and `stderr`\n* alternatively split `stdout` and `stderr`\n* strace console\n* console with only warning character (whatever that means)\n\n```sh\nttrace --timing <CMD>\n```\n\n\n### Other ideas\n\n* trace changes environment\n* trace docker image usage\n* highlight failed processes\n\n## Installation\n\n## Development & Contribution\n\n```\npip3 install -U poetry pre-commit\ngit clone --recurse-submodules https://projects.om-office.de/frans/ttrace.git\ncd ttrace\npre-commit install\n# if you need a specific version of Python inside your dev environment\npoetry env use /home/frafue/.pyenv/versions/3.10.4/bin/python3\npoetry install\n```\n\n## License\n\nFor all code contained in this repository the rules of GPLv3 apply unless\notherwise noted. That means that you can do what you want with the source\ncode as long as you make the files with their original copyright notice\nand all modifications available.\n\nSee [GNU / GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.\n\n\n## Read\n\n* [The Difference Between fork(), vfork(), exec() and clone()](https://www.baeldung.com/linux/fork-vfork-exec-clone)\n* [HN: The Magic of strace](https://news.ycombinator.com/item?id=7155799)\n* [The Magic of strace (archive.org)](https://web.archive.org/web/20160116001752/http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/)\n\n",
    'author': 'Frans Fürst',
    'author_email': 'frans.fuerst+gitlab@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://projects.om-office.de/frans/ttrace.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
