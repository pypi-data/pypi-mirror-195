# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docstring_builder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'docstring-builder',
    'version': '0.1.0',
    'description': '',
    'long_description': '# docstring_builder\n\nHere be dragons.\n',
    'author': 'Alistair Miles',
    'author_email': 'alimanfoo@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
