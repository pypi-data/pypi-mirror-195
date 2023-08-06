# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web',
 'web.env',
 'web.env.database',
 'web.errors',
 'web.kernel',
 'web.kernel.messaging',
 'web.kernel.proc',
 'web.trend',
 'web.trend.grpc',
 'web.trend.rest',
 'web.trend.rest.utils',
 'web.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.5,<2.0.0',
 'tortoise-orm[asyncpg]>=0.19.3,<0.20.0']

setup_kwargs = {
    'name': 'web-foundation',
    'version': '3.0.0',
    'description': 'python web-server template',
    'long_description': '',
    'author': 'yaroher',
    'author_email': 'yaroher2442@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
