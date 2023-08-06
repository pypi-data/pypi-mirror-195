# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['exmc']

package_data = \
{'': ['*']}

install_requires = \
['clipboard>=0.0.4,<0.0.5']

entry_points = \
{'console_scripts': ['exmc = exmc.__main__:main']}

setup_kwargs = {
    'name': 'exmc',
    'version': '0.0.3',
    'description': 'Excel Markdown Converter',
    'long_description': "# Excel Markdown Converter\n\n[![PyPI](https://img.shields.io/pypi/v/exmc.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/exmc.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/exmc)][pypi status]\n[![License](https://img.shields.io/pypi/l/exmc)][license]\n\n[![Read the documentation at https://exmc.readthedocs.io/](https://img.shields.io/readthedocs/exmc/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/idlewith/exmc/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/exmc/\n[read the docs]: https://exmc.readthedocs.io/\n[tests]: https://github.com/idlewith/exmc/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/idlewith/exmc\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- copy excel content from clipboard, so you need paste excel content to clipboard\n- type `exmc` to convert excel string to markdown table string\n- type `exmc -r` convert markdown table string to excel string\n\n## Requirements\n\n- `clipboard`\n\n## Installation\n\nYou can install _Excel Markdown Converter_ via [pip] from [PyPI]:\n\n```console\n$ pip install exmc\n```\n\n## Usage\n\ndemo video below\n\nhttps://user-images.githubusercontent.com/61551277/215328281-79cb339f-8d92-4c11-91a3-a6ba54642c24.mp4\n\nthe details below\n\n- `exmc`\n\ncopy content from excel sheet\n\ntype `exmc` in terminal/cmd,\n\nthen markdown table string will copy to clipboard automatically\n\nso you can paste in markdown file\n\n- `exmc -r`\n\n-r stands for reverse\n\nuse `-r` flag convert markdown table string to excel string\n\nso, you need copy raw markdown table string\n\nthen paste to excel file\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Excel Markdown Converter_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/idlewith/exmc/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/idlewith/exmc/blob/main/LICENSE\n[contributor guide]: https://github.com/idlewith/exmc/blob/main/CONTRIBUTING.md\n[command-line reference]: https://exmc.readthedocs.io/en/latest/usage.html\n",
    'author': 'idlewith',
    'author_email': 'newellzhou@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/idlewith/exmc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
