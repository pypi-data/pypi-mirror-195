# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trr_ds_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trr-ds-core',
    'version': '0.0.0a0',
    'description': 'dummy trr-ds-core',
    'long_description': '',
    'author': 'Scyther',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
