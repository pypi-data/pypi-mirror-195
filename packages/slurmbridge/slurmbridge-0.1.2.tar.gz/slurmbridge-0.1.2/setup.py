# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurmbridge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slurmbridge',
    'version': '0.1.2',
    'description': 'A Django ORM Style Bridge to Local Slurm Commands',
    'long_description': None,
    'author': 'Griesshaber Daniel',
    'author_email': 'griesshaber@hdm-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
