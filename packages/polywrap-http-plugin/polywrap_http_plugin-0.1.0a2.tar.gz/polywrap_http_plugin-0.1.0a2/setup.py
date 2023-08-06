# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_http_plugin']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0',
 'polywrap-client==0.1.0a11',
 'polywrap-plugin==0.1.0a11']

setup_kwargs = {
    'name': 'polywrap-http-plugin',
    'version': '0.1.0a2',
    'description': '',
    'long_description': '# Polywrap HTTP Plugin',
    'author': 'Niraj Kamdar',
    'author_email': 'niraj@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
