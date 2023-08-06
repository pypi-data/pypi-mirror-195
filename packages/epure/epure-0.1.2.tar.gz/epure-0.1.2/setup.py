# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_stub']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0', 'jsonpickle>=2.2.0,<3.0.0', 'psycopg2==2.9.3']

setup_kwargs = {
    'name': 'epure',
    'version': '0.1.2',
    'description': 'purest architecture',
    'long_description': None,
    'author': 'Nikita Umarov',
    'author_email': 'nagvalhm@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
