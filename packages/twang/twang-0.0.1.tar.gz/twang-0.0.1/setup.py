# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twang', 'twang.source_separation', 'twang.track', 'twang.util']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.33,<0.30.0',
 'ipython>=8.10.0,<9.0.0',
 'librosa>=0.10.0,<0.11.0',
 'mido>=1.2.10,<2.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'pydub>=0.25.1,<0.26.0',
 'ruff>=0.0.254,<0.0.255']

setup_kwargs = {
    'name': 'twang',
    'version': '0.0.1',
    'description': 'Making it easy to mess with music & machine learning',
    'long_description': '',
    'author': 'mhsb',
    'author_email': 'michael.h.s.ball@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/michaelhball/twang',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
