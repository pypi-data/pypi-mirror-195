# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hackblitz', 'hackblitz.clients', 'hackblitz.clients.ingress']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hackblitz',
    'version': '0.1.0',
    'description': 'HackBlitz SDK',
    'long_description': None,
    'author': 'Satheesh Kumar',
    'author_email': 'mail@satheesh.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
