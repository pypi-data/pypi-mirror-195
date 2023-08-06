# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfn_guard_rs_hook']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'cfn-guard-rs>=0.2.1,<0.3.0',
 'cloudformation-cli-python-lib>=2.1.12,<3.0.0',
 'jsonpath-rw>=1.0.0,<2.0.0',
 'pyyaml>=5.4.1,<5.5.0']

setup_kwargs = {
    'name': 'cfn-guard-rs-hook',
    'version': '0.2.2',
    'description': 'Works with cloudformation-cli-python-lib to remove duplicate code when creating a CloudFormation registry hook that leverages the library cfn_guard_rs',
    'long_description': None,
    'author': 'Kevin DeJong',
    'author_email': 'kddejong@amazon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
