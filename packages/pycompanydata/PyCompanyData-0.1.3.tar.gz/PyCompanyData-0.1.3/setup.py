# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycompanydata',
 'pycompanydata.clients',
 'pycompanydata.data_types',
 'pycompanydata.data_types.accounting',
 'pycompanydata.data_types.platform',
 'pycompanydata.handlers',
 'pycompanydata.handlers.accounting',
 'pycompanydata.handlers.platform']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.1.1,<6.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'types-toml>=0.10.8.5,<0.11.0.0']

setup_kwargs = {
    'name': 'pycompanydata',
    'version': '0.1.3',
    'description': 'A Python client library for interacting with the Codat API',
    'long_description': 'None',
    'author': 'Peter Simpson',
    'author_email': 'peter_joseph_simpson@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
