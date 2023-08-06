# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nodelib', 'nodelib.types']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.2.1,<6.0.0',
 'hexbytes>=0.3.0,<0.4.0',
 'py-automapper>=1.2.3,<2.0.0',
 'tronpy>=0.2.6,<0.3.0',
 'web3>=5.31.3,<6.0.0']

setup_kwargs = {
    'name': 'nodelib',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'farirat',
    'author_email': 'fourat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
