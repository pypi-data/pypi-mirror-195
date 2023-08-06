# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyseek']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pyseek = pyseek.__main__:app']}

setup_kwargs = {
    'name': 'pyseek',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Zach Lopez',
    'author_email': 'zachlopez9@gmail.com',
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
