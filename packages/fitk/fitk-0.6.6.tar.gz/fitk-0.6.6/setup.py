# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitk', 'fitk.interfaces']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.11"': ['matplotlib>=3.5,<4.0'],
 ':python_version == "3.7"': ['numpy==1.21.6', 'scipy==1.7.3'],
 ':python_version >= "3.11"': ['matplotlib>=3.6,<4.0'],
 ':python_version >= "3.8"': ['numpy>1.22', 'scipy>1.7.3']}

setup_kwargs = {
    'name': 'fitk',
    'version': '0.6.6',
    'description': 'The Fisher Information ToolKit',
    'long_description': 'None',
    'author': 'JCGoran',
    'author_email': 'goran.jelic-cizmek@unige.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
