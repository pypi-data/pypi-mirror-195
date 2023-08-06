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
    'version': '2023.3.3.post2',
    'description': '',
    'long_description': '# AiShell 🤖\n\n[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)\n[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)\n\n\nA simple Python code that connects to OpenAI\'s ChatGPT and executes the returned results.\n\n## Demo\n\n![Demo](https://raw.githubusercontent.com/code-yeongyu/AiShell/master/images/example.gif)\n\n## Key Features 💡\n\n- Interact with your computer using natural language\n- Automatically executes the command from the response of ChatGPT\n- Good for complex tasks like handling Git and extracting tar files\n- No need to search StackOverflow for commands, AiShell has got you covered\n- **No need to set up annoying retrieving of tokens or API keys with ChatGPT, as AiShell does it for you. INSTALL IT. EXECUTE IT. DONE.**\n\n## Prerequisites 📚\n\n- Python 3.9+\n- ChatGPT Account (or OpenAI Account)\n\n## Installation 🔧\n\n```sh\npip install aishell\n```\n\n## Getting Started 🚀\n\nLet\'s just start by printing "Hello World" using AiShell.\n\n```sh\naishell \'print Hello World\'\n```\n\n## Advanced Settings 🛠\n\n### For those who want to use `Official ChatGPT(GPT3.5-turbo)` or `GPT-3`\n\n1. Create account on OpenAI\n1. Go to <https://platform.openai.com/account/api-keys>, Copy API key\n1. Modify or create `~/.aishell/config.json` file like following\n\n    ```sh\n    {\n        ...\n        "language_model": <language model of your preference>, //"official_chatgpt" or "gpt3"\n        "openai_api_key": <your openai api key>\n    }\n    ```\n\n## Contributions 💬\n\nFeel free to contribute to AiShell by adding more functionality or fixing bugs.\n',
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
