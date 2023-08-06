# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picle']

package_data = \
{'': ['*']}

install_requires = \
['pydantic==1.10.4']

extras_require = \
{':sys_platform == "win32"': ['pyreadline3==3.4.1'],
 'docs:python_version >= "3.7"': ['mkdocs==1.2.4',
                                  'mkdocs-material==7.2.2',
                                  'mkdocs-material-extensions==1.0.1',
                                  'mkdocstrings[python]>=0.18.0,<0.19.0',
                                  'pygments==2.11',
                                  'pymdown-extensions==9.3']}

setup_kwargs = {
    'name': 'picle',
    'version': '0.1.0',
    'description': 'Python Interactive Command Line Shells',
    'long_description': None,
    'author': 'Denis Mulyalin',
    'author_email': 'd.mulyalin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
