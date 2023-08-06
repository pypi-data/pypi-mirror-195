# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nc', 'nc.palette', 'nc.palette.terminal16']

package_data = \
{'': ['*']}

install_requires = \
['xmod>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'nc',
    'version': '1.0.0',
    'description': '🎨 Named colors in Python 🎨',
    'long_description': "NC is a collection of named colors that acts like both an array and\n    a dictionary, used to replace `sys.modules['nc']`.\n\n\n### [API Documentation](https://rec.github.io/nc#nc--api-documentation)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
