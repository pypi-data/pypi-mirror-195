# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_chat']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'openai>=0.27.0,<0.28.0',
 'prompt-toolkit>=3.0.38,<4.0.0',
 'rich>=13.3.1,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['cli-chat = cli_chat.app:app',
                     'cli-chat-config = cli_chat.app:config_app']}

setup_kwargs = {
    'name': 'cli-chat',
    'version': '0.2.1',
    'description': '',
    'long_description': '## `cli-chat`\n\n`cli-chat` is a command-line tool that allows you to have a conversation with ChatGPT from your terminal. Follow the simple steps below to install and use this tool.\n\n### Installation\n\n#### Mac\n\n`cli-chat` can be installed on Mac using [Homebrew](https://brew.sh/). To install `cli-chat` using Homebrew, \nsimply execute the following command in your terminal:\n\n```bash\nbrew tap tefx/tap\nbrew install cli-chat\n```\n\n#### Other Platforms\n\nTo install `cli-chat`, execute the following command in your terminal:\n\n```bash\npip install cli-chat\n```\n\nAlternatively, you can clone the repository and install the dependencies using `poetry`. Here are the steps to follow:\n\n1. Install [poetry](https://python-poetry.org/docs/#installation).\n2. Clone the repository.\n3. Navigate to the repository\'s root directory.\n4. Execute `poetry install`.\n\n### Usage\n\nTo start a conversation with ChatGPT, execute the following command in your terminal:\n\n```bash\ncli-chat\n```\n\nAlternatively, you can start the script by executing the following command in your terminal:\n\n```bash\npoetry run cli-chat\n```\n\nHere are a few things to keep in mind when using `cli-chat`:\n\n- Before being able to use the tool, you must obtain an API key by registering for it [here](https://platform.openai.com/account/api-keys).\n- To end the conversation, type "thanks", "thx", or a similar phrase.\n- You can navigate through your conversation history with the arrow keys.\n- Common key-bindings and auto-suggestions are supported, thanks to [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).\n\n### Control Commands\n\nYou can use special control commands to modify `cli-chat`\'s behavior. These commands should be placed at the beginning of your question string and should start with a backslash `\\\\`.\n\nThe supported control commands are listed below:\n\n| Command       | Arguments | Tags             | Description                                                                                                                                                     |\n|---------------|-----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| `\\no-render`  |           |                 | Prevent the answer from being rendered in markdown.                                                                                                             |\n| `\\load-file`  |           |                 | Load a file and use the contents as the remaining part of your question.                                                                                         |\n| `\\long`       |           |                 | Accept multi-line inputs from now on. Use <kbd>Meta</kbd>+<kbd>Enter</kbd> or <kbd>ESC</kbd> followed by <kbd>Enter</kbd> to finish.                            |\n| `\\save`       |           | `append`        | Save the last answer to a file.                                                                                                                                 |\n| `\\hide-answer`|           |                 | Do not show the answer. **WARNING: Always check the answer first to avoid losing it if you want to save it later.**                                           |\n| `\\continue`   | `idx`     |                 | Resume the conversation from a previous answer. `idx` should be a negative number as shown by the `\\history` command.                                          |\n| `\\forget`     |           |                 | Delete your conversation history.                                                                                                                               |\n| `\\history`    |           |                 | Show your entire conversation history.                                                                                                                          |\n\nYou can combine multiple control commands by separating them with `|`. For instance, `\\no-render|load-file` will load a file and prevent the answer from being rendered in markdown.\n\nFor some commands, additional arguments and tags may be specified by using the syntax `command(arg1, arg2, ...){tag1, tag2, ..}`. For example, `\\save{append}` will append the answer to the file instead of overwriting it, while `\\continue(-1)` will resume the conversation from the answer with index `-1` in the history.\n\n### Example\n\nHere are a few examples of what a conversation with `cli-chat` might look like:\n\n![Example 1](./docs/example-1.png)\n\n![Example 2](./docs/example-2.png)\n\n![Example 3](./docs/example-3.png)\n\n![Example 4](./docs/example-4.png)\n\n## Configuration\n\nUse `cli-chat-config` to manage key and input history.',
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
