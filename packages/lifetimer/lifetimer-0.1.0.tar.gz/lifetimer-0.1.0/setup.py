# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lifetimer', 'lifetimer.config']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'platformdirs>=3.0.0,<4.0.0', 'yaspin>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['lifetimer = lifetimer.cli:execute_from_command_line']}

setup_kwargs = {
    'name': 'lifetimer',
    'version': '0.1.0',
    'description': 'Lifespan timer',
    'long_description': "# Lifetimer\n\n[![PyPI version](https://img.shields.io/pypi/v/lifetimer)](https://pypi.org/project/lifetimer/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/lifetimer)](https://pypi.org/project/lifetimer/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis is a lifespan timer that allows you to watch the seconds tick down to the time you set for yourself.\n\nIt's for anyone who wants to feel the time dwindle, push themselves to get up to speed on their studies and work.\n\n## Installation\n\n```sh\npip install lifetimer\n```\n\n## Usage\n\nWhen installed, you have to set your last date and time of your life through `lifetimer` or `lifetimer init` commands.\n\nIf you want to change the settings, use `lifetimer init` command.\n\n```sh\n$ lifetimer init\nPlease, enter your last date and time of your life.\nYear: 2100\nMonth [12]: 3\nDay [31]: 6\nHour [23]: 17\nMinute [59]: 58\nSecond [59]: 50\n```\n\nAfter settings, when you want to check your lifespan, just type `lifetimer` command.\n\n```sh\n$ lifetimer\n🕛 You have 2,455,857,087 seconds to live.\n```\n",
    'author': 'kimfame',
    'author_email': 'renownkim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kimfame/lifetimer.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
