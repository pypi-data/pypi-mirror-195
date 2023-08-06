import time
import click

USER_COLOR="white"
BOT_COLOR="blue"

def get_role_color(role):
    return USER_COLOR if role == "user" else BOT_COLOR

def print_message(message):
    click.echo(click.style("> ", fg=BOT_COLOR), nl=False)

    message["content"] = message["content"].strip()

    for character in message["content"]:
        click.echo(click.style(character, fg=BOT_COLOR), nl=False)
        time.sleep(0.02)

    click.echo()
    click.echo()

def print_error(error):
    click.echo(click.style("[ERROR] {}\n".format(error), fg="red"))