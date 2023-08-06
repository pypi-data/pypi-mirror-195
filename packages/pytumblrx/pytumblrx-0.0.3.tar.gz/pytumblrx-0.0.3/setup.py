# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytumblrx']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.2.0,<2.0.0', 'httpx>=0.23.3,<0.24.0', 'strenum>=0.4.9,<0.5.0']

extras_require = \
{'full': ['Pillow>=9.4.0,<10.0.0']}

setup_kwargs = {
    'name': 'pytumblrx',
    'version': '0.0.3',
    'description': 'A Python Tumblr API v2 Client based on httpx with async support',
    'long_description': 'None',
    'author': 'dj-ratty',
    'author_email': '115014503+dj-ratty@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dj-ratty/pytumblrx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
