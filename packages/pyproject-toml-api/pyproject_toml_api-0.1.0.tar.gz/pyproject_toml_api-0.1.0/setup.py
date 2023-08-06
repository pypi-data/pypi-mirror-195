# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyproject_toml_api', 'pyproject_toml_api.version_api']

package_data = \
{'': ['*']}

install_requires = \
['semantic-version>=2.10.0,<3.0.0']

extras_require = \
{'dev': ['mypy>=1.0.1,<2.0.0', 'tox>=4.4.6,<5.0.0', 'pytest>=7.2.1,<8.0.0'],
 'docs': ['sphinx>=5.3,<6.0',
          'myst-parser>=0.18,<0.19',
          'sphinx-rtd-theme>=1.2.0,<2.0.0']}

setup_kwargs = {
    'name': 'pyproject-toml-api',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Pyproject.toml API\n',
    'author': 'Zack Hankin',
    'author_email': 'zthankin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
