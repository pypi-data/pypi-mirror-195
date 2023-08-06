# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whisper_cli']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.0,<0.28.0', 'toml>=0.10.2,<0.11.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['whisper = whisper_cli.main:app']}

setup_kwargs = {
    'name': 'whisper-cli',
    'version': '0.0.2',
    'description': "A command-line interface for transcribing and translating audio using OpenAI's Whisper API",
    'long_description': "# Whisper CLI\nWhisper CLI is a command-line interface for transcribing and translating audio using OpenAI's Whisper API. It also allows you to manage multiple OpenAI API keys as separate environments.\n\nTo install Whisper CLI, simply run:\n\n```sh\npip install whisper-cli\n```\n\n## Setup\nTo get started with Whisper CLI, you'll need to set your OpenAI API key. You can do this using the following command:\n\n```sh\nwhisper set-key <openai_api_key>\n```\n\nThis will set the API key for the default environment. If you want to use a different API key, you can set up an alternative environment by running:\n\n```sh\nwhisper set-key <openai_api_key> --env <env_name>\n```\n\nTo activate an alternative environment, run:\n\n```sh\nwhisper activate-env <env_name>\n```\n\n## Usage\n\nWhisper CLI supports two main functionalities: translation and transcription.\n\n### Translation\nTo translate an audio file, simply run:\n\n```sh\nwhisper translate <file_name>\n```\n\n### Transcription\nTo transcribe an audio file, run:\n\n```sh\nwhisper transcribe <file_name>\n```\n\n## Development\nIf you'd like to contribute to Whisper CLI, you'll need to set up a development environment with Python 3.10.9.\n\n```sh\npython=3.10.9\n```\n\nHappy transcribing and translating with Whisper CLI.\n",
    'author': 'Vatsal',
    'author_email': 'vatsalaggarwal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
