# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sakkara',
 'sakkara.model',
 'sakkara.model.composable',
 'sakkara.model.composable.group',
 'sakkara.model.composable.hierarchical',
 'sakkara.model.fixed',
 'sakkara.relation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23,<2.0',
 'pandas>=1.4,<2.0',
 'pymc>=5.0.0,<6.0.0',
 'pytensor>=2.9.1,<3.0.0']

setup_kwargs = {
    'name': 'sakkara',
    'version': '0.3.0',
    'description': 'Tools for fast creation of PyMC models',
    'long_description': 'None',
    'author': 'Henrik Håkansson',
    'author_email': 'henrik.hakansson@fcc.chalmers.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
