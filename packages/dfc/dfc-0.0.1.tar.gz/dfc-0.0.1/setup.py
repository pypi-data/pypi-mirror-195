# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dfc',
    'version': '0.0.1',
    'description': 'Data Format Converter',
    'long_description': 'DFC : Data Format Converter',
    'author': 'Sumanth',
    'author_email': 'sumanthreddystar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
