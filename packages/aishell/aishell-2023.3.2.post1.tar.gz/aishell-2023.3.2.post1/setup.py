# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aishell',
 'aishell.models',
 'aishell.query_clients',
 'aishell.tests',
 'aishell.utils']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.26.5,<0.27.0',
 'poetry>=1.3.1,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyright>=1.1.294,<2.0.0',
 'revchatgpt>=2.2.7,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aishell = aishell:main']}

setup_kwargs = {
    'name': 'aishell',
    'version': '2023.3.2.post1',
    'description': '',
    'long_description': "# AiShell 🤖\n\n[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)\n[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)\n\n\nA simple Python code that connects to OpenAI's ChatGPT and executes the returned results.\n\n## Demo\n\n![Demo](images/example.gif)\n\n## Key Features 💡\n\n- Interact with your computer using natural language\n- Automatically executes the command from the response of ChatGPT\n- Good for complex tasks like handling Git and extracting tar files\n- No need to search StackOverflow for commands, AiShell has got you covered\n\n## Installation 🔧\n\n```sh\npip install aishell\n```\n\n## Usage 📝\n\n```sh\naishell --help\n```\n\n## Prerequisites 📚\n\n- Python 3.9.5\n- Poetry\n- OpenAI API Key\n\n## Getting Started 🚀\n\n### For those who want to use reverse-engineered `ChatGPT`\n\n1. Login on <https://chat.openai.com/>\n1. Get your 'accessToken` from <https://chat.openai.com/api/auth/session>\n1. `export CHATGPT_ACCESS_KEY=<your access token>`\n1. Enjoy AiShell\n\n### For those who want to use `GPT-3`\n\n1. Create account on OpenAI\n1. Go to <https://platform.openai.com/account/api-keys>, Copy API key\n1. Set the API key as an environment variable `OPENAI_API_KEY` or inject it directly into the code by editing it.\n1. Enjoy AiShell\n\n### For those who want to use Official ChatGPT API `gpt-3.5-turbo`\n\n- Currently not supported, but soon will be supported!\n\n## Contributions 💬\n\nFeel free to contribute to AiShell by adding more functionality or fixing bugs.\n",
    'author': 'None',
    'author_email': 'None',
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
