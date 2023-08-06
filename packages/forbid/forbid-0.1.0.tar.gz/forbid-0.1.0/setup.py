# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forbid', 'forbid.contrib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'forbid',
    'version': '0.1.0',
    'description': '',
    'long_description': '# forbid\n\nYet another test project\n',
    'author': 'Vlad Dmitrievich',
    'author_email': '2tunnels@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/2tunnels/forbid',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
