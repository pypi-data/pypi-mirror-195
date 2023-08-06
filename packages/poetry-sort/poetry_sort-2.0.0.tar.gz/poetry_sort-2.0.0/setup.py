# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_sort']

package_data = \
{'': ['*']}

install_requires = \
['dict-deep>=4.1.2,<5.0.0', 'poetry>=1.2,<2.0', 'pydantic>=1.10.2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['sort = poetry_sort.plugin:PoetrySortPlugin']}

setup_kwargs = {
    'name': 'poetry-sort',
    'version': '2.0.0',
    'description': 'Alphabetically sort your Poetry dependencies',
    'long_description': '# poetry-sort\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-sort?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-sort)\n[![PyPI](https://img.shields.io/pypi/v/poetry-sort?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-sort)\n[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/celsiusnarhwal/poetry-sort?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-sort/releases)\n[![PyPI - License](https://img.shields.io/pypi/l/poetry-sort?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-sort/blob/main/LICENSE.md)\n[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)\n\npoetry-sort is a [Poetry](https://python-poetry.org/) plugin that alphabetically sorts the dependencies in\nyour `pyproject.toml` file.\n\n## Installation\n\n```bash\npoetry self add poetry-sort\n```\n\n## Usage\n\n```bash\npoetry sort\n```\n\n`poetry sort` supports the `--with`, `--without`, and `--only` options, which function identically to `poetry install`.\nFor full usage information, run `poetry sort --help`.\n\npoetry-sort runs automatically whenever you run `poetry add` or `poetry init` and will sort only the dependency\ngroups that were modified by the command.\n\n## Configuration\n\nYou can configure poetry-sort via the `tool.poetry.sort` section of `pyproject.toml`.\n\n```toml\n[tool.sort.config]\nauto = true\ncase-sensitive = false\nsort-python = false\nformat = true\n\n```\n\nThe following options are available:\n\n- `auto` (`bool`, default: `true`): Whether or not to automatically sort dependencies when running `poetry add`\n  or `poetry init`. `poetry sort` can always be run manually, regardless of this setting.\n\n- `case-sensitive` (`bool`, default: `false`): Whether to take case into account when sorting.\n\n- `sort-python` (`bool`, default: `false`): Whether to also sort the `python` dependency. If `false`, the `python`\n  dependency will be placed at the top of `tool.poetry.dependencies`; if `true`, it will be sorted alphebetically with\n  everything else.\n\n- `format` (`bool`, default: `true`): Whether to apply some basic formatting to `pyproject.toml` after sorting.\n  If `true`, poetry-sort will :take all occurences of three or more consecutive newlines in `pyproject.toml` and\n  replace them with two newlines.\n\n## License\n\npoetry-sort is licensed under the [MIT License](https://github.com/celsiusnarhwal/poetry-sort/blob/main/LICENSE.md).\n',
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/celsiusnarhwal/poetry-sort',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
