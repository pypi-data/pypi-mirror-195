# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streambot']

package_data = \
{'': ['*']}

install_requires = \
['sseclient-py>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'streambot',
    'version': '0.1.0',
    'description': 'An OpenAI ChatGPT wrapper to simplify streaming of token responses to give the writing effect.',
    'long_description': None,
    'author': 'dr00',
    'author_email': 'andrewmeyer23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
