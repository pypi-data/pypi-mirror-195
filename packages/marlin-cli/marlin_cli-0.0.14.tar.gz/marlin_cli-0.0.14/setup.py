# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['marlin_cli', 'marlin_cli.api', 'marlin_cli.commands', 'marlin_cli.util']

package_data = \
{'': ['*']}

install_requires = \
['cfn-flip>=1.3.0,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'gitpython>=3.1.30,<4.0.0',
 'pre-commit>=3.0.4,<4.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['marlin = marlin_cli.marlin:cli']}

setup_kwargs = {
    'name': 'marlin-cli',
    'version': '0.0.14',
    'description': '',
    'long_description': "# Marlin: The fastest path to modern web apps\n\n90% of software is the exact same; the final 10% is what differentiates a product. Marlin helps developers build the first 90% fast, so they can focus on what matters.\n\n## Installation\n\nMarlin can be built from source with the included build.sh script. Run the script and a single file executable will be written to `./dist/marlin`. Add this to your path or envoke it directly.\n\n## Documentation\n\nEventually we're going to put docs here\n\n## Contribute\n\nMarlin-cli uses pyenv for environment management and Poetry for dependcy management. These can be installed with the included `dev_setup.sh` script.\n\n\n## VSCode\n\nOpen VSCode and run the following commands in the terminal\n```\npoetry shell\npoetry env info --path | pbcopy\n```\n\nOpen the VSCode command palette with `cmd+shift+P` and search for `Python: select interpretor`. Open it, click `Enter interpreter path...` and paste the path copied from poetry above.",
    'author': 'George Cooper',
    'author_email': 'george@marlincode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.11.1',
}


setup(**setup_kwargs)
