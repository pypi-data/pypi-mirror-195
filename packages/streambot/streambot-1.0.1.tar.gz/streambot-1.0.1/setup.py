# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streambot']

package_data = \
{'': ['*']}

install_requires = \
['sseclient-py>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'streambot',
    'version': '1.0.1',
    'description': 'An OpenAI ChatGPT wrapper to simplify streaming of token responses to give the writing effect.',
    'long_description': '# StreamBot\nStreamBot is a Python package that allows you to create a chatbot that uses OpenAI\'s GPT-3 API to generate responses in real-time.\n\n## Installation\nTo install StreamBot, simply run:\n\n```shell\npip install streambot\n```\n\n## Usage\nTo create a StreamBot, you\'ll need to provide an OpenAI API key, a name for your bot, and a "genesis prompt" - the initial message that your bot will respond to.\n\n```python\nfrom streambot import StreamBot\n\napi_key = "YOUR_OPENAI_API_KEY"\nbot_name = "MyBot"\ngenesis_prompt = "Hello, how can I help you today?"\n\nbot = StreamBot(api_key, bot_name, genesis_prompt)\nOnce you have created your bot, you can start chatting with it using the chat method. The chat method takes a list of messages as input and returns a string containing the bot response.\n```\n\n```python\nresponse = bot.chat(["Hi there!", "What\'s your name?"])\nprint(response)\n```\n\nYou can also add messages to your bot\'s message history using the add_message method.\n\n```python\nbot.add_message("Hello, how can I help you today?", role="system")\nbot.add_message("Hi there!", role="user")\nbot.add_message("What\'s your name?", role="user")\n```\n\n## Configuration\nStreamBot also allows you to configure various settings for your bot, such as the temperature and maximum number of tokens used by the GPT-3 API. To do this, you can create a StreamBotConfig object and pass it to the StreamBot constructor.\n\n```python\nfrom streambot import StreamBot, StreamBotConfig\n\napi_key = "YOUR_OPENAI_API_KEY"\nbot_name = "MyBot"\ngenesis_prompt = "Hello, how can I help you today?"\n\nconfig = StreamBotConfig(temperature=0.5, max_tokens=50)\n\nbot = StreamBot(api_key, bot_name, genesis_prompt, config=config)\n```\n\n## Contributing\nIf you\'d like to contribute to StreamBot, please feel free to submit a pull request or open an issue on the GitHub repository.\n\n## License\nStreamBot is licensed under the MIT License. See LICENSE for more information.',
    'author': 'dr00',
    'author_email': 'andrewmeyer23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dr00-eth/StreamBot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
