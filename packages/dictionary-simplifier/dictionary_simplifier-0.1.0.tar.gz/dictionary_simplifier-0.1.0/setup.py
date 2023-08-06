# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictionary_simplifier']

package_data = \
{'': ['*']}

install_requires = \
['bandit>=1.7.4,<2.0.0',
 'black>=23.1.0,<24.0.0',
 'flake8>=6.0.0,<7.0.0',
 'isort>=5.12.0,<6.0.0',
 'pytest>=7.2.2,<8.0.0']

setup_kwargs = {
    'name': 'dictionary-simplifier',
    'version': '0.1.0',
    'description': 'Simplify python dictionary operations with custom function',
    'long_description': '# Introduction',
    'author': 'Md. Sany Ahmed',
    'author_email': 'sany2k8@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.9,<4.0.0',
}


setup(**setup_kwargs)
