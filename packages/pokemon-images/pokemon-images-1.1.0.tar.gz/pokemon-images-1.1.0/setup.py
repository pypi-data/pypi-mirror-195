# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokemon_images']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pokemon-images',
    'version': '1.1.0',
    'description': 'Randomly get images of Pokémon from the official Pokémon website',
    'long_description': '# `pokemon_images.py`\n\nA small library with no dependencies to get a random image of a Pokémon.\n\nUsage is simple: `import pokemon_images`, then `pokemon_images.get_random_url`.\n\n## Some notes\n\nThere are no accented `é`s in this library to aid typing on keyboards that do not have this key. In all cases, `é` should be replaced by `e` except in documentation.\n\nThis library is fully typed and fully documented with Python docstrings.\n\nContributions are welcome, but this library is considered feature-complete.\n',
    'author': 'Tomodachi94',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
