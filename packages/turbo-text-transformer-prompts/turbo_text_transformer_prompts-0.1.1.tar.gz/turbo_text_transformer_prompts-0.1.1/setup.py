# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tttp']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['tttp = tttp.__main__:main']}

setup_kwargs = {
    'name': 'turbo-text-transformer-prompts',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Turbo Text Transformer Prompts\n\nPrompts for [Turbo Text Transformer](https://github.com/fergusfettes/turbo-text-transformer).\n',
    'author': 'fergus',
    'author_email': 'fergusfettes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
