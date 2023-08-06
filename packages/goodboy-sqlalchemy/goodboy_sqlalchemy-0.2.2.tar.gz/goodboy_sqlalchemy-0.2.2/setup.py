# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goodboy_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['goodboy>=0.2,<0.3', 'sqlalchemy']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['typing-extensions>=4.0']}

setup_kwargs = {
    'name': 'goodboy-sqlalchemy',
    'version': '0.2.2',
    'description': 'Data validation tool for SQLALchemy',
    'long_description': '# Goodboy-SQLAlchemy: Data Validation for SQLAlchemy\n\nThis project is currently in an early stage of development.',
    'author': 'Maxim Andryunin',
    'author_email': 'maxim.andryunin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
