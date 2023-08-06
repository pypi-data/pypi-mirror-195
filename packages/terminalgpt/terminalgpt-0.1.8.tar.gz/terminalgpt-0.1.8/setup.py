# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminalgpt']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0', 'openai>=0.27.0,<0.28.0', 'tiktoken>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['terminalgpt = terminalgpt.main:main']}

setup_kwargs = {
    'name': 'terminalgpt',
    'version': '0.1.8',
    'description': 'AI chat asistent in your terminal powered by OpenAI GPT-3.5',
    'long_description': "# TerminalGPT\n\nWelcome to the terminal-based ChatGPT personal assistant app! With the terminalGPT command, you can easily interact with ChatGPT and receive short, easy-to-read answers on your terminal.\n\nChatGPT is specifically optimized for your machine's operating system, distribution, and chipset architecture, so you can be sure that the information and assistance you receive are tailored to your specific setup.\n\nWhether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.\n\nThank you for using TerminalGPT, and we hope you find the terminal-based app to be a valuable resource for your day-to-day needs!\n\n# Installation and Usage\n\n1. Install the package with pip install.\n\n```sh\npip install terminalgpt -U\n```\n\n2. (Optional) Inject the token to the executable script on your local machine so you don't have to export it every time you open a new terminal\n\n```sh\ngit clone https://github.com/adamyodinsky/TerminalGPT.git\ncd TerminalGPT\nexport OPENAI_API_KEY=<YOUR_OPEN_AI_KEY>\n./inject_token.sh\n```\n\nNote: When not using the inject_token.sh script, you will need to export the OPENAI_API_KEY environment variable with your open AI token every time you open a new terminal.\n\n## Usage\n\n```sh\nterminalgpt\n```\n",
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
