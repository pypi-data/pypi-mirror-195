# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_auth_tacacs']

package_data = \
{'': ['*']}

install_requires = \
['tacacs_plus>=2.6,<3.0']

setup_kwargs = {
    'name': 'django-auth-tacacs',
    'version': '0.0.1',
    'description': 'Tacacs+ external authentication backend for Django - Nautbot - Netbox',
    'long_description': "# django-auth-tacacs\n\nA django authentication backend that uses Tacacs+ for authentication. This can also be used with Nautobot or Netbox.\n\n## Description\n\nThis backend authenticates users via Tacacs+. Only authentication is implemented, authorization is expected to be managed within the application itself, depending on the user groups.\n\nUsers that don't exist yet may be added automatically by enabling the option `TACACSPLUS_AUTOCREATE_USERS`. Newly created users will be added with the standard django parameters `is_admin=False` and `is_staff=False`.\n\nIf you have customized User tables then this package may not work as expected.\n\n## Installation\n\nInstall the package with pip:\n\n```python\npip3 install django-auth-tacacs\n```\n\nThis package requires `tacacs-plus` to be installed.\n\nDepending on the usage, it also requires one of the following packages:\n\n- django\n- nautobot\n- netbox\n\n## Usage\n\nTo use this package, you'll need to add the `TACACSPlusAuthenticationBackend` library to the `AUTHENTICATION_BACKENDS` configuration parameter. The order is important, if you have multiple authentication backends then you must configure them in the correct order.\n\nYou also need to add the `TACACS_PLUS` configuration parameters:\n\n```python\nTACACSPLUS_HOST = 'localhost'\nTACACSPLUS_PORT = 49\nTACACSPLUS_SECRET = 'super-secret'\nTACACSPLUS_SESSION_TIMEOUT = 5\nTACACSPLUS_AUTH_PROTOCOL = 'ascii'\nTACACSPLUS_AUTOCREATE_USERS = True\n```\n\n### Django example\n\nThis example will use the Tacacs+ authentication backend and fallback to the internal django DB user authentication:\nAdd the following to `settings.py`\n\n```python\nAUTHENTICATION_BACKENDS = [\n    'django_auth_tacacs.django.TACACSPlusAuthenticationBackend',\n    'django.contrib.auth.backends.ModelBackend',\n]\nTACACSPLUS_HOST = 'localhost'\nTACACSPLUS_PORT = 49\nTACACSPLUS_SECRET = 'super-secret'\nTACACSPLUS_SESSION_TIMEOUT = 5\nTACACSPLUS_AUTH_PROTOCOL = 'ascii'\nTACACSPLUS_AUTOCREATE_USERS = True \n```\n\n### Nautobot example\n\nThis example will use the Tacacs+ authentication backend and fallback to the internal nautobot DB user authentication.  \nAdd the following to `nautobot_config.py`\n\n```python\nAUTHENTICATION_BACKENDS = [\n     'django_auth_tacacs.nautobot.TACACSPlusAuthenticationBackend',\n     'nautobot.core.authentication.ObjectPermissionBackend',\n]\nTACACSPLUS_HOST = 'localhost'\nTACACSPLUS_PORT = 49\nTACACSPLUS_SECRET = 'super-secret'\nTACACSPLUS_SESSION_TIMEOUT = 5\nTACACSPLUS_AUTH_PROTOCOL = 'ascii'\nTACACSPLUS_AUTOCREATE_USERS = True \n```\n\n### Netbox example\n\nThis example will use the Tacacs+ authentication backend and fallback to the internal netbox DB user authentication.  \nAdd the following to `configuration.py`\n\n```python\nREMOTE_AUTH_BACKEND = 'django_auth_tacacs.nautobot.TACACSPlusAuthenticationBackend'\n\nTACACSPLUS_HOST = 'localhost'\nTACACSPLUS_PORT = 49\nTACACSPLUS_SECRET = 'super-secret'\nTACACSPLUS_SESSION_TIMEOUT = 5\nTACACSPLUS_AUTH_PROTOCOL = 'ascii'\nTACACSPLUS_AUTOCREATE_USERS = True \n```\n",
    'author': 'Maarten Wallraf',
    'author_email': 'mwallraf@2nms.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
