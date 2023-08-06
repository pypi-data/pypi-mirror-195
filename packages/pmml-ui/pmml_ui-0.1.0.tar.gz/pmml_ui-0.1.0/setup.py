# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pmml_ui', 'pmml_ui.auth', 'pmml_ui.mailing_lists', 'pmml_ui.updater']

package_data = \
{'': ['*'],
 'pmml_ui': ['templates/*', 'templates/auth/*', 'templates/mailing_lists/*']}

install_requires = \
['Flask>=2.2.3,<3.0.0',
 'flask-wtf>=1.1.1,<2.0.0',
 'kubernetes>=26.1.0,<27.0.0',
 'werkzeug>=2.2.3,<3.0.0',
 'wtforms[email]>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'pmml-ui',
    'version': '0.1.0',
    'description': 'Web ui for pmml',
    'long_description': '# pmmml-ui\n',
    'author': 'Michael Wilson',
    'author_email': 'mw@1wilson.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
