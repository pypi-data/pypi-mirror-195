# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fatld']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'oapackage>=2.7.6,<3.0.0',
 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'fatld',
    'version': '0.1.0',
    'description': 'Generate and characterize designs with four-and-two-level (FATL) factors',
    'long_description': 'None',
    'author': 'Alexandre Bohyn',
    'author_email': 'alexandre.bohyn@kuleuven.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://abohyndoe.github.io/fatld/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
