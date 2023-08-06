# The prompter takes a jinja2 template and a dictionary of values and
# returns a string with the template rendered with the values.

import jinja2
from pathlib import Path


class Prompter:
    def __init__(self, filename):
        self.template = Path(filename).read_text()

    def prompt(self, prompt, args=None):
        args = args or {'prompt': prompt} 
        args.update({'prompt': prompt}) 
        return jinja2.Template(self.template).render(args)

    @staticmethod
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
