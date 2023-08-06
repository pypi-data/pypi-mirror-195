# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_chat']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.0,<0.28.0',
 'prompt-toolkit>=3.0.38,<4.0.0',
 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['cli-chat = cli_chat:main']}

setup_kwargs = {
    'name': 'cli-chat',
    'version': '0.1.0',
    'description': '',
    'long_description': '# cli-chat\n\ncli-chat is a command-line tool that allows you to have a conversation with ChatGPT from your terminal.\n\n## Installation\n\nTo install cli-chat, follow these steps:\n\n1. Clone the repository.\n2. Run `poetry install` to install the dependencies.\n\n## Usage\n\nTo start a conversation, run the following command in your terminal:\n```\n# poetry run cli-chat\n```\n\n\n### Notes:\n\n1. You will need a valid API key from [here](https://platform.openai.com/account/api-keys) to use the tool.\n2. The key will be stored in a file named `.key` in the same directory as the script. If you want to change the key or stop using the script, simply remove this file.\n3. You can use the arrow keys to navigate through the history of your conversation.\n4. To end the conversation, simply type "thanks", "thx", or something similar.\n5. If you don\'t want to render the conversation history as markdown in the terminal, put `[nm]` in front of your question. \nFor example, if you want to ask "How are you?" without rendering it as markdown, you would type `[nm] How are you?` instead.\n\n## Example\n\n![Example](docs/example-1.png)\n\n![Example](./docs/example-2.png)',
    'author': 'Zhu Zhaomeng',
    'author_email': 'zhaomeng.zhu@ntu.edu.sg',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
