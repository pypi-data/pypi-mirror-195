import click

from app.models.chat import Chat

from app.utils.consts import ERROR_MESSAGE
from app.utils.cache import load_key, save_key
from app.utils.print import print_error
from app.utils.validation import is_valid_key

@click.command()
@click.option("-k", "--key", prompt="Enter your OpenAI API key")
def main(key=None):
    if not key:
        key = load_key()

    elif is_valid_key(key):
        save_key(key)

    else:
        print_error(ERROR_MESSAGE["bad_format_key"])
        quit()

    click.echo()
    chat = Chat(key)

    while True:
        prompt = click.prompt("", prompt_suffix="> ")

        if prompt == "!quit":
            break

        chat.send_message(prompt)
