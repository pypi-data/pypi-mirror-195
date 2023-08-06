# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn', 'fn.dialect', 'fn.dialect.click', 'fn.standard']

package_data = \
{'': ['*']}

extras_require = \
{'click': ['click>=8.1.3,<9.0.0'], 'full': ['click>=8.1.3,<9.0.0']}

setup_kwargs = {
    'name': 'ifn',
    'version': '0.1.3',
    'description': 'Function Interface Toolbox',
    'long_description': None,
    'author': 'Iydon Liang',
    'author_email': 'liangiydon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iydon/ifn',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
