#!/usr/bin/env python3

from pathlib import Path

import click

from tttp.prompter import Prompter


def arg2dict(args):
    d = {}
    if '=' not in args:
        return d
    for arg in args.split(','):
        k, v = arg.split("=")
        d[k] = v
    return d


def find_file(filename):
    # Look in './general', '../general', in '~/.config/ttt/templates', and '~/.config/tttp/templates'
    # and subdirectories
    paths = [
        Path.cwd() / 'templates',
        Path.cwd().parent / 'templates', 
        Path.home() / ".config/ttt/templates",
        Path.home() / ".config/tttp/templates/templates"
    ]

    # Make sure file ends with 'j2'
    if not filename.endswith(".j2"):
        filename += ".j2"

    for path in paths:
        if not path.exists():
            continue
        if (path / filename).exists():
            return path / filename
        for p in path.iterdir():
            if p.is_dir() and (p / filename).exists():
                return p / filename
    raise FileNotFoundError(f"File {filename} not found. Looked in {paths} and subdirectories.")


@click.command()
@click.option("--filename", "-f", help="Name of the template to use.", default="empty")
@click.option("--prompt", "-p", help="Prompt to use.", default="")
@click.option("--args", "-x", help="Extra values for the template.", default="")
def main(filename, prompt, args):
    filename = find_file(filename)
    args = arg2dict(args)

    # If there is no prompt, try to get it from stdin
    if not prompt:
        prompt = click.get_text_stream("stdin").read().strip()
        if not prompt:
            return

    sink = click.get_text_stream("stdout")

    prompter = Prompter(filename, prompt, args)
    completion = prompter.prompt()

    sink.write(completion)
