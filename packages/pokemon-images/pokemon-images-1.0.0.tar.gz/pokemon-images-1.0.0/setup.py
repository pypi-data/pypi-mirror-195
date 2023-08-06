# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokemon_images']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pokemon-images',
    'version': '1.0.0',
    'description': 'Randomly get images of Pokémon from the official Pokémon website',
    'long_description': None,
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
