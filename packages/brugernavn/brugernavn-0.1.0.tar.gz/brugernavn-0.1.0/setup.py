# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brugernavn']

package_data = \
{'': ['*'], 'brugernavn': ['ressources/*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'brugernavn',
    'version': '0.1.0',
    'description': 'A OSINT tool to search for a username on many websites',
    'long_description': '# Brugernavn\n\nBrugernavn is a OSINT tool to search for user names at websites.\nYou can find the project [here](https://edugit.org/pinguin/brugernavn).\nBrugernavn is licensed under the MIT License, the document can be found [here](https://edugit.org/pinguin/brugernavn/-/blob/master/LICENSE).',
    'author': 'Jonathan Krüger',
    'author_email': 'jonathan.krueger@teckids.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://edugit.org/pinguin/brugernavn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
