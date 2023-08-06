# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyshapley']

package_data = \
{'': ['*']}

install_requires = \
['deprecated>=1.2.10,<2.0.0',
 'importlib-metadata>=4.4,<5.0',
 'importlib-resources>=5.0,<6.0',
 'numpy>=1.22,<2.0',
 'semantic_version>=2.10,<3.0']

setup_kwargs = {
    'name': 'pyshapley',
    'version': '0.1.0',
    'description': 'Library for computing Shapley values of coalitional games',
    'long_description': '# pyshapley [![PyPI version](https://badge.fury.io/py/pyshapley.svg)](https://badge.fury.io/py/pyshapley) ![Tests](https://github.com/JulianStier/pyshapley/workflows/Tests/badge.svg) [![Downloads](https://pepy.tech/badge/pyshapley)](https://pepy.tech/project/pyshapley) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)\n\n\n## Installation\n- With **pip** from PyPi: ``pip install pyshapley``\n- With **conda** in your *environment.yml* (recommended for reproducible experiments):\n```yaml\nname: exp01\nchannels:\n- defaults\ndependencies:\n- pip>=20\n- pip:\n    - pyshapley\n```\n- With **poetry** (recommended for *projects*) using PyPi: ``poetry add pyshapley``\n- From public GitHub: ``pip install --upgrade git+ssh://git@github.com:JulianStier/pyshapley.git``\n',
    'author': 'Julian Stier',
    'author_email': 'julian.stier@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JulianStier/pyshapley',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
