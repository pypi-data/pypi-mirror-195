# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixieai', 'fixieai.agents', 'fixieai.client']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'fastapi[all]>=0.89.1,<0.90.0',
 'gql[all]>=3.4.0,<4.0.0',
 'prompt-toolkit>=3.0.31,<4.0.0',
 'pydantic',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['fixie = fixieai.client.console:fixie']}

setup_kwargs = {
    'name': 'fixieai',
    'version': '0.1.7',
    'description': 'SDK for the Fixie.ai platform. See: https://fixie.ai',
    'long_description': 'None',
    'author': 'Fixie.ai Team',
    'author_email': 'hello@fixie.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
