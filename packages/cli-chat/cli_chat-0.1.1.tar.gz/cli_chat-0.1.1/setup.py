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
    'version': '0.1.1',
    'description': '',
    'long_description': '# cli-chat\n\n`cli-chat` is a powerful command-line tool that allows you to have a conversation with ChatGPT from your terminal. Follow the simple steps below to install and use this tool.\n\n## Installation\n\nYou can easily install `cli-chat` by typing the following command in your terminal:\n\n```bash\npip install cli-chat\n```\n\nAlternatively, you can clone the repository and install the dependencies using `poetry`. Follow the steps below:\n\n1. Clone the repository.\n2. Run `poetry install`.\n\n## Usage\n\nTo start a conversation, simply type the following command in your terminal:\n\n```bash\ncli-chat\n```\n\nAlternatively, start the script using `poetry` by typing the following command in your terminal:\n\n```bash\npoetry run cli-chat\n```\n\nHere are a few things to keep in mind when using `cli-chat`:\n\n* Before using the tool, you must obtain an API key from [here](https://platform.openai.com/account/api-keys).\n* The API key will be saved in a file named `.key` in your current directory. To change the key or stop using the tool, simply delete this file.\n* You can use arrow keys to navigate through your conversation history.\n* To end the conversation, type "thanks", "thx", or a similar phrase.\n* Common key-bindings and auto-suggestions are supported, thanks to [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).\n\n### Control Sequences\n\nYou can use special control sequences to modify the behavior of the tool. A sequence is always placed at the beginning of your question string and starts with a backslash `\\`.\n\nThe following control sequences are available:\n\n| Sequence     | Description                                                                                        |\n|--------------|----------------------------------------------------------------------------------------------------|\n| `\\no-render` | Do not render the answer\'s markdown.                                                               |\n| `\\load-file` | Load a file and use its contents as the next question.                                             |\n| `\\long`      | Accept multi-line inputs starting from now on.                                                     |\n| `\\save`      | Save the last answer in a file.                                                                    |\n| `\\hide-answer`| Do not show the answer. **Danger: If you want to save the answer later, always check it.**" |\n\nYou can use multiple control sequences at once by separating them with commas. For example, `\\no-render,load-file` will load a file and not render its contents as markdown.\n\n## Example\n\nHere are a couple of examples of what a conversation with `cli-chat` might look like:\n\n![Example 1](./docs/example-1.png)\n\n![Example 2](./docs/example-2.png)\n\n![Example 3](./docs/example-3.png)',
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
