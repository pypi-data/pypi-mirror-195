# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminalgpt']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0', 'openai>=0.27.0,<0.28.0', 'tiktoken>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['terminalgpt = terminalgpt:main']}

setup_kwargs = {
    'name': 'terminalgpt',
    'version': '0.1.0',
    'description': 'AI chat asistent in your terminal powered by OpenAI GPT-3.5',
    'long_description': '',
    'author': 'Adam Yodinsky',
    'author_email': '27074934+adamyodinsky@users.noreply.github.com',
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
