#!python3
import subprocess
from typing import List

import click
import inquirer
from requests import get as getr

API_URI = 'https://www.codegrepper.com/api/search.php?q={prompt}&search_options=search_titles'
LANGS = ['', 'sh', 'shell', 'bash', 'linux', 'zsh']


def is_command(res) -> bool:
    return res['language'] in LANGS or '$' in res['answer']


def filter_choices_and_explanations(result) -> List[str]:
    choices = []
    for count, res in enumerate(result, start=1):
        if not is_command(res):
            continue
        explanation = []
        command = []
        is_broken = False
        for line in res['answer'].split("\n"):
            line = line.strip()
            if line.startswith("#"):
                line = line.replace('#', '', 1)
                explanation.append(line)
                continue
            if not is_broken:
                if line.startswith("$"):
                    is_broken = True
                    line = line.replace("$", "", 1)
                command.append(line)
        if explanation:
            other_explanations = '\n '.join(explanation[1:])
            explans = f'{count}. {explanation[0]}\n{other_explanations}'
            click.echo(explans)
        if command:
            choices.append(' && '.join(command))
    return choices


def get_result(prompt) -> list:
    result = []
    for prefix in LANGS:
        result = getr(API_URI.format(
            prompt=f'{prefix} {prompt}')).json().get('answers')
        if result:
            break
    return result


@click.command()
@click.argument("prompt", nargs=-1)
def search(prompt):
    prompt = ' '.join(prompt)
    result = get_result(prompt)
    choices = filter_choices_and_explanations(result)
    if not choices:
        return click.secho('No results found for "{}"'.format(prompt), fg="yellow")
    options = [
        inquirer.List(
            'option',
            message='Choose command to run',
            choices=choices,
            default=None
        ),
    ]
    answer = inquirer.prompt(options)
    if answer:
        subprocess.run(answer['option'], shell=True)


if __name__ == '__main__':
    search()
