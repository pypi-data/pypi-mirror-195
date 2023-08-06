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
    'version': '0.5.0',
    'description': '',
    'long_description': '# vk_fetch\n\nScript helps to fetch all data from your VK account\n',
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
