# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chattr_config',
 'chattr_config.config_loader',
 'chattr_config.config_loader.config',
 'chattr_config.decorators',
 'chattr_config.log_formatter',
 'chattr_config.monitoring',
 'chattr_config.monitoring.service',
 'chattr_config.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'boto3>=1.9.201',
 'click>=8.1.3,<8.2.0',
 'datadog==0.44.0',
 'ddtrace>=1.9.0,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'singleton-decorator>=1.0.0,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'chattr-config',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chattr',
    'author_email': 'chattra23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
