# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calitp_data_analysis']

package_data = \
{'': ['*']}

install_requires = \
['calitp-data==2023.2.13.1',
 'geopandas>=0.12.2,<0.13.0',
 'ipython>=8.9.0,<9.0.0',
 'jinja2<3.1.0',
 'pandas-gbq>=0.19.1,<0.20.0',
 'pendulum>=2.1.2,<3.0.0',
 'siuba>=0.4.2,<0.5.0',
 'sqlalchemy-bigquery>=1.6.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'calitp-data-analysis',
    'version': '2023.3.3',
    'description': 'Shared code for querying Cal-ITP data in notebooks, primarily.',
    'long_description': 'None',
    'author': 'Andrew Vaccaro',
    'author_email': 'andrew.v@jarv.us',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
