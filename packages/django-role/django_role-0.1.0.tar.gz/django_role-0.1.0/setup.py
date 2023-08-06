# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['user_role', 'user_role.migrations']

package_data = \
{'': ['*'], 'user_role': ['templates/forms/widgets/*']}

install_requires = \
['django>=4.1.7,<5.0.0']

setup_kwargs = {
    'name': 'django-role',
    'version': '0.1.0',
    'description': 'Role for django User model',
    'long_description': '# django-user-role\nRole for django User model\n',
    'author': 'isys35',
    'author_email': 'isys35@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
