# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cached_classproperty']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cached-classproperty',
    'version': '0.3.0',
    'description': '',
    'long_description': 'None',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
