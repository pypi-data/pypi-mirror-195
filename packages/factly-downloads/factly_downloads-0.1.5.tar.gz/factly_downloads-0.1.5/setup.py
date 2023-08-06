# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factly', 'factly.downloads']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.20,<2.0.0', 'click>=8.0.0,<9.0.0']

entry_points = \
{'console_scripts': ['wbu = factly.downloads.wasabi_bulk_upload:main']}

setup_kwargs = {
    'name': 'factly-downloads',
    'version': '0.1.5',
    'description': '',
    'long_description': 'None',
    'author': 'Factly Labs',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
