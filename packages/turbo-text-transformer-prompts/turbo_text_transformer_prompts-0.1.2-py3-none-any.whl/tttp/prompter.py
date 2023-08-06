# The prompter takes a jinja2 template and a dictionary of values and
# returns a string with the template rendered with the values.

import jinja2
from pathlib import Path


class Prompter:
    def __init__(self, filename, prompt, args=None):
        self.template = Path(filename).read_text()
        self.args = args or {'prompt': prompt} 
        self.args.update({'prompt': prompt}) 

    def prompt(self):
        return jinja2.Template(self.template).render(self.args)
