# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numpydoc_decorator']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions']

setup_kwargs = {
    'name': 'numpydoc-decorator',
    'version': '0.6.0',
    'description': '',
    'long_description': '# numpydoc_decorator\n\nThis package allows you to build numpy-style docstrings\nprogrammatically and apply them using a decorator. This can be useful\nbecause:\n\n* Parts of your documentation, such as parameter descriptions, can be\n  shared between functions, avoiding the need to repeat yourself.\n\n* Type information for parameters and return values is automatically\n  picked up from type annotations and added to the docstring, avoiding\n  the need to maintain type information in two places.\n\nWork in progress.\n\n\n## Installation\n\n`pip install numpydoc_decorator`\n\n\n## Examples\n\n@@TODO\n',
    'author': 'Alistair Miles',
    'author_email': 'alimanfoo@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
