# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kimfame']

package_data = \
{'': ['*']}

install_requires = \
['faker>=17.0.0,<18.0.0']

entry_points = \
{'console_scripts': ['kimfame = kimfame.kimfame:main',
                     'triplea = kimfame.aaa:aaa',
                     'tripled = kimfame.ddd:ddd']}

setup_kwargs = {
    'name': 'kimfame',
    'version': '0.0.28',
    'description': 'PyPI test project',
    'long_description': '# Kimfame\n\n[![PyPI version](https://img.shields.io/pypi/v/kimfame)](https://pypi.org/project/kimfame/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/kimfame)](https://pypi.org/project/kimfame/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPyPI Test Project\n\n"Hello world"\n\n"How are you?"\n',
    'author': 'kimfame',
    'author_email': 'renownkim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kimfame/kimfame',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
