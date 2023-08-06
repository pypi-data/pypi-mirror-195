# cli-chat

cli-chat is a command-line tool that allows you to have a conversation with ChatGPT from your terminal.

## Installation

To install cli-chat, follow these steps:

1. Clone the repository.
2. Run `poetry install` to install the dependencies.

## Usage

To start a conversation, run the following command in your terminal:
```
# poetry run cli-chat
```


### Notes:

1. You will need a valid API key from [here](https://platform.openai.com/account/api-keys) to use the tool.
2. The key will be stored in a file named `.key` in the same directory as the script. If you want to change the key or stop using the script, simply remove this file.
3. You can use the arrow keys to navigate through the history of your conversation.
4. To end the conversation, simply type "thanks", "thx", or something similar.
5. If you don't want to render the conversation history as markdown in the terminal, put `[nm]` in front of your question. 
For example, if you want to ask "How are you?" without rendering it as markdown, you would type `[nm] How are you?` instead.

## Example

![Example](docs/example-1.png)

![Example](./docs/example-2.png)