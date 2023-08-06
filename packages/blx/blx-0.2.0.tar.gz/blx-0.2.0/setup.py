# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blx']

package_data = \
{'': ['*']}

install_requires = \
['minio>=7.1.13',
 'pydantic>=1.10.5',
 'python-dotenv>=0.21.0',
 'typer[all]>=0.7.0']

entry_points = \
{'console_scripts': ['blx = blx.cli:app']}

setup_kwargs = {
    'name': 'blx',
    'version': '0.2.0',
    'description': 'Make BLOBs globally accessible',
    'long_description': '# blx\n\nMake BLOBs globally accessible.\n',
    'author': 'Danilo Horta',
    'author_email': 'danilo.horta@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
