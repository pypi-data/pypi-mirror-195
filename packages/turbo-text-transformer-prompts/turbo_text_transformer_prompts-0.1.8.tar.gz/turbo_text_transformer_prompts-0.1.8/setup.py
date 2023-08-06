# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tttp']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'ipython>=8.10.0,<9.0.0', 'jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['tttp = tttp.__main__:main']}

setup_kwargs = {
    'name': 'turbo-text-transformer-prompts',
    'version': '0.1.8',
    'description': '',
    'long_description': '# Turbo Text Transformer Prompts\n\nNote this is automatically installed when you do `pip install turbo-text-transformer`. This repo is just for storing the templates.\n\nDesigned for use with [turbo-text-transformer](https://github.com/fergusfettes/turbo-text-transformer).\n\nYou pipe some text in, the template is applied, then you pipe it into `ttt` (from `pip install turbo-text-transformer`) which will process it with eg. OpenAI.\n\n```\ncat pyproject.toml tttp/__main__.py | tttp -t readme | ttt > README.md\n```\n\nTurbo Text Transformer Prompts is a command-line tool that allows users to generate text files from pre-configured templates using user input prompts. The tool uses Jinja2 templating engine to render text files from templates.\n\n## How to Run\n\n```sh\npip install turbo-text-transformer-prompts\n```\n\nYou will also need to clone the repository containing the templates you want to use. For example:\n\n```sh\nmkdir -p ~/.config/ttt/\ngit clone https://github.com/fergusfettes/turbo-text-transformer-prompts ~/.config/ttt\n```\n\n## Template Structure\n\nA template is a text file written in Jinja2 syntax. The file should have the `.j2` extension and be placed inside the `templates` directory. They will be installed in the `~/.config/ttt/templates` directory.\n\nThis is a smiple example of a template:\n\n```jinja\nContext: Provide only code as output.\nPrompt: {{prompt}}\nCode:\n```\n\nIt will just output a code snippet based on the query.\n\nYou can also pass a list of flags to the prompt to fine tune the control, such as this:\n\n```jinja\nThis is an example of minimally altering some given code to achieve a specific task.\n\nI received the following code:\n\n`{{language}}\n{{prompt}}\n`\n\nMy task was to make minimal alterations to this code to: "{{task}}".\n\nThe altered code is below.\n\n`{{language}}\n```\n\nFor this one, you can pass the \'task\' and \'language\' arguments to make it more specific.\n\n## Contributing\n\nPULL REQUESTS WITH MORE TEMPLATES VERY WELCOME!\n\nIf you find a bug or would like to contribute to Turbo Text Transformer Prompts, please create a new GitHub issue or pull request.\n\n#  License\n\nTurbo Text Transformer Prompts is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.\n',
    'author': 'fergus',
    'author_email': 'fergusfettes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
