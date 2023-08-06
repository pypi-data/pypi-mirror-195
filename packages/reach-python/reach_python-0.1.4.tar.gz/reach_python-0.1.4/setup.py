# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reach_python', 'reach_python.http_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'reach-python',
    'version': '0.1.4',
    'description': '',
    'long_description': 'Package for https://github.com/lijian418/reach\n\n',
    'author': 'lijian418',
    'author_email': '126387358+lijian418@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
