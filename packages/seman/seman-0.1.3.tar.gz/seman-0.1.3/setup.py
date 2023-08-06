# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seman']

package_data = \
{'': ['*']}

install_requires = \
['cyclonedx-bom>=3.11.0,<4.0.0', 'fire>=0.5.0,<0.6.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['seman = seman.main:main']}

setup_kwargs = {
    'name': 'seman',
    'version': '0.1.3',
    'description': '',
    'long_description': '=================\nseman\n=================\n\nSemantics tools.\n\n.. image:: https://badge.fury.io/py/seman.svg\n    :target: https://badge.fury.io/py/seman\n\n.. image:: https://img.shields.io/pypi/dw/seman?style=flat\n    :target: https://pypistats.org/packages/seman\n\n.. image:: https://github.com/kannkyo/seman/actions/workflows/python-ci.yml/badge.svg\n    :target: https://github.com/kannkyo/seman/actions/workflows/python-ci.yml\n\n.. image:: https://github.com/kannkyo/seman/actions/workflows/scorecards.yml/badge.svg\n    :target: https://github.com/kannkyo/seman/actions/workflows/scorecards.yml\n',
    'author': 'kannkyo',
    'author_email': '15080890+kannkyo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kannkyo/seman',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
