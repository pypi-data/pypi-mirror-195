# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elysia']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0', 'pydantic>=1.10.5,<2.0.0']

setup_kwargs = {
    'name': 'elysia',
    'version': '1.0.0',
    'description': 'A better* way of creating attrs fields',
    'long_description': "# Elysia\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/elysia?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/elysia)\n[![PyPI](https://img.shields.io/pypi/v/elysia?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/elysia)\n[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/celsiusnarhwal/elysia?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/celsiusnarhwal/elysia/releases)\n[![PyPI - License](https://img.shields.io/pypi/l/elysia?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/elysia/blob/main/LICENSE.md)\n[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)\n\nElysia is an addon for [_attrs_](https://attrs.org) that provides what I think is a better API for defining instance\nattributes than _attrs_' own.\n\n## Installation\n\n```bash\npip install elysia\n```\n\n## Usage\n\nElysia's sole export is the `Fields` class, which wraps `attrs.field`, `attrs.setters`, and `attrs.validators` to\nprovide a more concise API for defining instance attributes.\n\nHere's a brief example of a class created with _attrs_ and Elysia:\n\n```python\nfrom datetime import datetime\n\nfrom attrs import define\nfrom elysia import Fields\n\n\n@define\nclass User:\n    name: str = Fields.field()\n    password: str = Fields.field(\n        on_setattr=Fields.setters.validate,\n        validator=Fields.validators.min_len(8)\n    )\n\n    created_at: datetime = Fields.attr(factory=datetime.utcnow, frozen=True)\n```\n\nThe `User` class has two `__init__` arguments: `name` and `password`. Whenever set, `password` is validated to\nensure it's at least 8 characters long.\n\n`User` also has a `created_at` attribute that can't set via an `__init__` argument. When a `User` object is\ninstantiated, `created_at` is set to the current time and cannot be changed afterwards.\n\n### So...how does all that work, exactly?\n\nGlad you asked.\n\nThere are two ways to define an attribute with Elysia: `Fields.field()` and `Fields.attr()`. `Fields.field()` defines\nattributes that map to `__init__` arguments; `Fields.attr()` defines attributes that do not. Both are wrappers around\n`attrs.field` and accept all the same arguments. Like `attrs.field`, all arguments to `Fields.field()`\nand `Fields.attr()` are keyword-only.\n\n> **Warning**\n>\n> `Fields.attr()` does not allow `default` to be `attrs.NOTHING` and `factory` to simultaneously be `None`, meaning\n> you **must** provide a value for one, and only one, of those arguments.\n\nBoth methods also accept an optional, boolean, `frozen` argument. Setting it to `True` is a shortcut\nfor `on_setattr=attrs.setters.frozen` — that is, it freezes the attribute, raising an exception if you try to set it\nafter initialization.\n\n> **Warning**\n>\n> Elysia is happy to combine `frozen=True` with anything else you pass to `on_setattr`, but `attrs.setters.frozen`\n> will be applied _first_, which may not be what you expect.\n\nFields also provides access to _attrs_' setters and validators via `Fields.setters` and `Fields.validators`,\nrespectively. It makes no difference whether setters and validators are accessed through `Fields` or `attrs`. Do what\nyou like.\n\n## License\n\nElysia is licensed under the [MIT License](https://github.com/celsiusnarhwal/elysia/blob/main/LICENSE.md).\n",
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/celsiusnarhwal/elysia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
