# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['workon_poetry']

package_data = \
{'': ['*'], 'workon_poetry': ['data/*']}

install_requires = \
['pip>=23,<24',
 'poetry>=1,<2',
 'python-dotenv>=0.21,<0.22',
 'virtualenv>=20,<21']

setup_kwargs = {
    'name': 'workon-poetry',
    'version': '0.0.1',
    'description': 'Natural Language Understanding (text processing) for math symbols, digits, and words with a Gradio user interface and REST API.',
    'long_description': '# workon-poetry\n\nBash and Python scripts to make switching and starting projects more efficient and less error-prone by automating some of the boring stuff and incorporating some opinions about best practices.\n\n## Dependencies\n\n* poetry\n* virtualenv\n\n## Setup your Python environment\n\nLaunch a `terminal` on Linux (or `git-bash` on Windows) then:\n\n1. Update your pip and virtualenv packages\n2. Clone the `workon-poetry` project\n3. Create a virtualenv within the `workon-poetry` dir\n4. Activate your new Python virtual environment\n5. Install this Python package in "--editable" mode\n\nAny Python version greater than `3.7` should work.\nMost Linux systems use Python `3.9` or higher: \n\n```bash\npip install --upgrade virtualenv poetry\ngit clone git@gitlab.com:tangibleai/community/workon-poetry\ncd workon-poetry\npython -m virtualenv --python 3.9 .venv\nls -hal\n```\n\nYou should see a new `.venv/` directory.\nIt will contain your python interpreter and a few `site-packages` like `pip` and `distutils`.\n\nNow activate your new virtual environment by sourcing `.venv/bin/activate` (on Linux) or `.venv/scripts/activate` (on Windows).\n\n```bash\n# bin/activate on Linux OR `Scripts/activate` in git-bash on Windows\nsource .venv/bin/activate || source .venv/Scripts/activate\n```\n\n## Developer install\n\nOnce you have a shiny new virtual environment activated you can install `workon-poetry` in `--editable` mode.\nThis way, when you edit the files and have the package change immediately.\n\nMake sure you are already within your cloned `workon-poetry` project directory.\nAnd makes sure your virtual environment is activated.\nYou should see the name of your virtual environment in parentheses within your command line prompt, like `(.venv) $`.\nThen when you install `workon-poetry` it will be available for import within any other Python application in that virtual environment.\n\n```bash\npip install --editable .\n```\n\n## User install\n\nIf you don\'t want to contribute, and you just want to **USE** `workon-poetry` the MathText modules, you can install it from a binary wheel on PyPi:\n\n```bash\npip install workon-poetry\n```\n\n',
    'author': 'Hobson Lane',
    'author_email': 'gitlab@totalgood.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tangibleai/community/workon-poetry',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
