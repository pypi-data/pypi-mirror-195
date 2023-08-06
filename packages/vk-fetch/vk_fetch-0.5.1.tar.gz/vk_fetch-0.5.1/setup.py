# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vk_fetch',
 'vk_fetch.commands',
 'vk_fetch.jobs',
 'vk_fetch.models',
 'vk_fetch.models.media_types']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich>=13.3.1,<14.0.0',
 'typer[rich]>=0.7.0,<0.8.0',
 'vk-api>=11.9.9,<12.0.0']

entry_points = \
{'console_scripts': ['vk_fetch = vk_fetch.run:app']}

setup_kwargs = {
    'name': 'vk-fetch',
    'version': '0.5.1',
    'description': '',
    'long_description': '# vk_fetch\n\n<p>\n    <img alt="license: MIT" src="https://img.shields.io/github/license/rmksrv/vk_fetch">\n    <img alt="python: 3.11" src="https://img.shields.io/badge/python-3.11-brightgreen">\n    <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</p>\n\nScript helps to fetch all data from your VK account. No need to browse every part of profile and \nmanually download every single file.\n\n\n## Usage\n\n```\nvk_fetch --help\n\n Usage: vk_fetch [OPTIONS] COMMAND [ARGS]...\n\n Script helps to fetch all data from your VK account\n\n╭─ Options ────────────────────────────────────────────────────────────────────╮\n│ --install-completion        [bash|zsh|fish|powershe  Install completion for  │\n│                             ll|pwsh]                 the specified shell.    │\n│                                                      [default: None]         │\n│ --show-completion           [bash|zsh|fish|powershe  Show completion for the │\n│                             ll|pwsh]                 specified shell, to     │\n│                                                      copy it or customize    │\n│                                                      the installation.       │\n│                                                      [default: None]         │\n│ --help                                               Show this message and   │\n│                                                      exit.                   │\n╰──────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ───────────────────────────────────────────────────────────────────╮\n│ download   Download data from VK profile                                     │\n│ ping       Check app can connect to VK and auth as user with login/pass      │\n│ show       Print available data of VK profile                                │\n╰──────────────────────────────────────────────────────────────────────────────╯\n```\n\n\n## Sample cases\n\n- Download all:\n![](docs/images/demo-download-all.png)\n- Download all exclude attachments in conversations `111`, `-222`, `c5`:\n![](docs/images/demo-download-all-except.png)\n- Download all attachments in conversations `111`, `-222`, `c5`:\n![](docs/images/demo-download-conversations.png)\n- Show all available data to fetch:\n![](docs/images/demo-show-all-available.png)\n',
    'author': 'Roman Kosarev',
    'author_email': 'rmksrv@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
