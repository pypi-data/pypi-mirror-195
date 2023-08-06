# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['startings']

package_data = \
{'': ['*']}

install_requires = \
['daemonprocessing>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'startings',
    'version': '0.1.0',
    'description': 'Register python scripts as bootstrapped',
    'long_description': 'Register python scripts as bootstrapped',
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
