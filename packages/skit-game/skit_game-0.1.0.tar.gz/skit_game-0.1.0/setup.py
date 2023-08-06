# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skit']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.4.0,<10.0.0']

setup_kwargs = {
    'name': 'skit-game',
    'version': '0.1.0',
    'description': 'A tool for prototyping card games',
    'long_description': '# Skit\n\nA tool for prototyping card games.\n\nInspired by [squib][squib], but I could never quite get my head around Ruby.\n\n[squib]: https://github.com/andymeneely/squib\n',
    'author': 'Matt Cooper',
    'author_email': 'vtbassmatt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
