# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsswapper']

package_data = \
{'': ['*'],
 'awsswapper': ['.mypy_cache/*',
                '.mypy_cache/3.9/*',
                '.mypy_cache/3.9/_typeshed/*',
                '.mypy_cache/3.9/collections/*',
                '.mypy_cache/3.9/ctypes/*',
                '.mypy_cache/3.9/email/*',
                '.mypy_cache/3.9/importlib/*',
                '.mypy_cache/3.9/importlib/metadata/*',
                '.mypy_cache/3.9/os/*']}

install_requires = \
['boto3>=1.17.75,<2.0.0', 'cliar>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['awsswapper = awsswapper:main']}

setup_kwargs = {
    'name': 'awsswapper',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
