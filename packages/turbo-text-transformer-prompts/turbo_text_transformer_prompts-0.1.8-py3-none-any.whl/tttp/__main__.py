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


@click.command()
@click.option("--filename", "-f", help="Name of the template to use.", default="empty")
@click.option("--prompt", "-p", help="Prompt to use.", default="")
@click.option("--args", "-x", help="Extra values for the template.", default="")
def main(filename, prompt, args):
    args = arg2dict(args)

    # If there is no prompt, try to get it from stdin
    if not prompt:
        prompt = click.get_text_stream("stdin").read().strip()
        if not prompt:
            return

    filename = Prompter.find_file(filename)
    completion = Prompter(filename).prompt(prompt, args)
    click.get_text_stream("stdout").write(completion)
