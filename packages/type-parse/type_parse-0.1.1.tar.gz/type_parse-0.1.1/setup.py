# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['type_parse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'type-parse',
    'version': '0.1.1',
    'description': 'Parse the markup language with Python type hints.',
    'long_description': '# type-parse\n',
    'author': 'nahco314',
    'author_email': 'nahco3_ta@yahoo.co.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
