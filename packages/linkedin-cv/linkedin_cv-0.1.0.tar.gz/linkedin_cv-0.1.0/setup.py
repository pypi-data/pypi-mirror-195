# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkedincv']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11.6,<0.12.0']

setup_kwargs = {
    'name': 'linkedin-cv',
    'version': '0.1.0',
    'description': 'Create LinkedIn inspired CVs from the command line',
    'long_description': '# linkedincv\n\n<p align="center">\n<a href="https://pypi.org/project/linkedin-cv" target="_blank">\n    <img src="https://img.shields.io/pypi/v/linkedin-cv?label=version&logo=python&logoColor=%23fff&color=306998" alt="PyPI - version">\n</a>\n\n<a href="https://pypi.org/project/linkedin-cv" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/linkedin-cv.svg?logo=python&logoColor=%23fff&color=306998" alt="PyPI - supported versions">\n</a>\n</p>\n\nCreate LinkedIn inspired CVs from the command line.\n\n## Installation\n\n`linkedin-cv` is available through PyPI:\n\n```bash\n  pip install linkedin-cv\n```\n',
    'author': 'ellsphillips',
    'author_email': 'elliott.phillips.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
