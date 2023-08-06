# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['chatcli']
install_requires = \
['fire>=0.5.0,<0.6.0',
 'openai>=0.27.0,<0.28.0',
 'prompt-toolkit>=3.0.38,<4.0.0']

entry_points = \
{'console_scripts': ['chatcli = chatcli:chatcli']}

setup_kwargs = {
    'name': 'chatcli',
    'version': '0.1.1',
    'description': "Streaming CLI interface for OpenAI's Chat API",
    'long_description': "# ChatCLI\n\nChatCLI is a Python script that provides an easy-to-use Command Line Interface (CLI) for OpenAI's Chat API. ChatCLI aims to provide a similar experience the ChatGPT frontend, including streaming tokens from the model as they are generated.\n\n```console\n$ chatcli\nChatCLI v0.1.0 | ↩ : submit | meta + ↩ : newline\n>>> Write 3 funny prompts for yourself.\n1. If you could only communicate through interpretive dance for the next 24 hours, how would you go about your day?\n\n2. You wake up in a world where everyone speaks in rhyme. How do you adapt to this unusual circumstance?\n\n3. You can only speak in questions for the rest of the day. How do you navigate conversations with friends, co-workers, and strangers?\n```\n\n## Installation\n\n```bash\npip install chatcli\n```\n\n## Usage\n\nRun `chatcli` from the command line.\n\nTo see the available options, run `chatcli --help`.\n\n```bash\n$ chatcli --help\nNAME\n    chatcli.py - Chat with an OpenAI API model using the command line.\n\nSYNOPSIS\n    chatcli.py <flags>\n\nDESCRIPTION\n    Chat with an OpenAI API model using the command line.\n\nFLAGS\n    --system=SYSTEM\n        Type: str\n        Default: 'You are a helpful as...\n        The system message to send to the model.\n    -a, --assistant=ASSISTANT\n        Type: Optional[Optional]\n        Default: None\n        The assistant message to send to the model.\n    --swap_newline_keys=SWAP_NEWLINE_KEYS\n        Type: bool\n        Default: False\n```\n\nOnce you start the script, you will be prompted to enter a message. Type your message and press the Enter key to send it to the OpenAI API model. The response from the model will be displayed on the screen.\n\n## License\n\nThis software is licensed under the MIT License.\n",
    'author': 'IsaacBreen',
    'author_email': 'mail@isaacbreen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
