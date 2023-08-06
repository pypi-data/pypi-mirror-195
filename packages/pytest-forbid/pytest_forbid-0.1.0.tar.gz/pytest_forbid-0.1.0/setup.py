# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_forbid']

package_data = \
{'': ['*']}

install_requires = \
['forbid>=0.1.2,<0.2.0', 'pytest>=7.2.2,<8.0.0']

entry_points = \
{'pytest11': ['forbid = pytest_forbid.plugin']}

setup_kwargs = {
    'name': 'pytest-forbid',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pytest-forbid\n\nYet another test project\n',
    'author': 'Vlad Dmitrievich',
    'author_email': '2tunnels@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
