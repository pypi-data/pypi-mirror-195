# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['type_enum_plugin']

package_data = \
{'': ['*']}

install_requires = \
['mypy']

setup_kwargs = {
    'name': 'type-enum-plugin',
    'version': '0.2.0',
    'description': 'Mypy plugin for type-enum.',
    'long_description': '# type-enum-plugin\n\nMypy plugin for TypeEnum.\n',
    'author': 'Thomas MK',
    'author_email': 'tmke8@posteo.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tmke8/type_enum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
