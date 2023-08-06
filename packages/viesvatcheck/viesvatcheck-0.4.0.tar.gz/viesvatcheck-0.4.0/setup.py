# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['viesvatcheck']

package_data = \
{'': ['*']}

install_requires = \
['zeep>=4.2.1,<5.0.0']

setup_kwargs = {
    'name': 'viesvatcheck',
    'version': '0.4.0',
    'description': '',
    'long_description': 'vies-vat-check\n==============================================\n\nPython client for https://ec.europa.eu/taxation_customs/vies/#/technical-information',
    'author': 'Mārtiņš Šulcs',
    'author_email': 'shulcsm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
