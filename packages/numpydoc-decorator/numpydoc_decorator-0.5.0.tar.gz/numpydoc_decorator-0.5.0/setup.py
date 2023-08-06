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
    'version': '0.5.0',
    'description': '',
    'long_description': '# numpydoc_decorator\n\nHere be dragons.\n',
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
