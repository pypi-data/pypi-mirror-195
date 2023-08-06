# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_drf']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.14.0,<4.0.0', 'flake8>=6.0.0,<7.0.0']

entry_points = \
{'flake8.extension': ['DRF = flake8_drf.plugin:Plugin']}

setup_kwargs = {
    'name': 'flake8-drf',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Sergei Konik',
    'author_email': 's.konik.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rocioar/flake8-drf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
