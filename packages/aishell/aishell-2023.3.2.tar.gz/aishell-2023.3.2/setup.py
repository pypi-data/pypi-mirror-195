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
    'version': '2023.3.2',
    'description': '',
    'long_description': "# AiShell 🤖\n\n[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)\n[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)\n\n\nA simple Python code that connects to OpenAI's ChatGPT and executes the returned results.\n\n## Key Features 💡\n\n- Interact with your computer using natural language\n- Automatically executes the command from the response of ChatGPT\n- Good for complex tasks like handling Git and extracting tar files\n- No need to search StackOverflow for commands, AiShell has got you covered\n\n### Simple Utility commands 🛠\n\n[![utility](https://asciinema.org/a/556670.svg)](https://asciinema.org/a/556670?speed=5)\n\n### A powerful git assistant 💪🏻👨\u200d💻💻\n\n[![git assistant](https://asciinema.org/a/556677.svg)](https://asciinema.org/a/556677?speed=5)\n\n## Installation 🔧\n\n```sh\npip install aishell\n```\n\n## Usage 📝\n\n```sh\npython -m aishell --help\n```\n\n## Prerequisites 📚\n\n- Python 3.9.5\n- Poetry\n- OpenAI API Key\n\n## Getting Started 🚀\n\n1. Create account on OpenAI\n1. Go to <https://platform.openai.com/account/api-keys>, Copy API key\n1. Set the API key as an environment variable `OPENAI_API_KEY` or inject it directly into the code by editing it.\n1. [Install](#installation)\n\n## Contributions 💬\n\nFeel free to contribute to AiShell by adding more functionality or fixing bugs.\n",
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
