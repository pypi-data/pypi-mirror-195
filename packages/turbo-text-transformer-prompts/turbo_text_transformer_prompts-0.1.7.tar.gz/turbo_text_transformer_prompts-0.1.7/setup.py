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
    'version': '0.1.7',
    'description': '',
    'long_description': '# Turbo Text Transformer Prompts\n\nDesigned for use with [turbo-text-transformer](https://github.com/fergusfettes/turbo-text-transformer).\n\nYou pipe some text in, the template is applied, then you pipe it into `ttt` which will process it with eg. OpenAI.\n\n```\ncat pyproject.toml tttp/__main__.py | tttp -t readme | ttt > README.md\n```\n\nTurbo Text Transformer Prompts is a command-line tool that allows users to generate text files from pre-configured templates using user input prompts. The tool uses Jinja2 templating engine to render text files from templates.\n\n## How to Run\n\n```sh\npip install turbo-text-transformer-prompts\n```\n\nYou will also need to clone the repository containing the templates you want to use. For example:\n\n```sh\nmkdir -p ~/.config/ttt/\ngit clone https://github.com/fergusfettes/turbo-text-transformer-prompts ~/.config/tttp\n```\n\n## Template Structure\n\nA template is a text file written in Jinja2 syntax. The file should have the `.j2` extension and be placed inside the `templates` directory.\n\nThe template can contain placeholders for user input. Placeholders are enclosed in double curly braces and contain a variable name. For example:\n\n```jinja\nHello, {{ name }}!\n```\n\nThis template will prompt the user to enter a value for the `name` variable.\n\n## Prompt Files\n\nPrompt files can be used to predefine the values to be filled in the template. Prompt files are text files that contain a prompt message followed by the values to be filled, one per line. For example:\n\n```\nPlease enter your name:\nJohn Doe\n```\n\nTo use a prompt file, specify the file using the `--prompt` option:\n\n```sh\ntttp --filename simple --prompt /path/to/prompt/file\n```\n\nIf there are any values that need to be added or changed from\n\n## Contributing\n\nIf you find a bug or would like to contribute to Turbo Text Transformer Prompts, please create a new GitHub issue or pull request.\n\n#  License\n\nTurbo Text Transformer Prompts is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.\n',
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
