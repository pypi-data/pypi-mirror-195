# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chattr_auth', 'chattr_auth.auth0_jwt', 'chattr_auth.chattr_jwt']

package_data = \
{'': ['*']}

install_requires = \
['pyjwt[crypto]>2,<3']

setup_kwargs = {
    'name': 'chattr-auth',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chattr',
    'author_email': 'chattra23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
