# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aishell',
 'aishell.adapters',
 'aishell.adapters.test',
 'aishell.exceptions',
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
 'pyperclip>=1.8.2,<2.0.0',
 'pyright>=1.1.294,<2.0.0',
 'revchatgpt>=3.0.5,<4.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'yt-dlp>=2023.2.17,<2024.0.0']

entry_points = \
{'console_scripts': ['aishell = aishell:main']}

setup_kwargs = {
    'name': 'aishell',
    'version': '2023.3.3.post1',
    'description': '',
    'long_description': "# AiShell 🤖\n\n[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)\n[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)\n\n\nA simple Python code that connects to OpenAI's ChatGPT and executes the returned results.\n\n## Demo\n\n![Demo](https://raw.githubusercontent.com/code-yeongyu/AiShell/master/images/example.gif)\n\n## Key Features 💡\n\n- Interact with your computer using natural language\n- Automatically executes the command from the response of ChatGPT\n- Good for complex tasks like handling Git and extracting tar files\n- No need to search StackOverflow for commands, AiShell has got you covered\n\n## Installation 🔧\n\n```sh\npip install aishell\n```\n\n## Usage 📝\n\n```sh\naishell --help\n```\n\n## Prerequisites 📚\n\n- Python 3\n- OpenAI API Key or ChatGPT Account\n\n## Getting Started 🚀\n\n### For those who want to use reverse-engineered `ChatGPT`\n\n- Permanent Login Method\n    1. Login on <https://chat.openai.com/>\n    1. Get your 'accessToken` from <https://chat.openai.com/api/auth/session>\n    1. Set the API key as an environment variable `CHATGPT_ACCESS_TOKEN`\n- Temporary Login Method\n    1. Just run `aishell <query>`\n    1. Browser opens up. Login there.\n    1. Tell AiShell which browser you use.\n    1. Enjoy AiShell\n\n### For those who want to use `Official ChatGPT(GPT3.5-turbo)` or `GPT-3`\n\n1. Create account on OpenAI\n1. Go to <https://platform.openai.com/account/api-keys>, Copy API key\n1. Set the API key as an environment variable `OPENAI_API_KEY`\n1. Enjoy AiShell\n\n## Contributions 💬\n\nFeel free to contribute to AiShell by adding more functionality or fixing bugs.\n",
    'author': 'None',
    'author_email': 'None',
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
