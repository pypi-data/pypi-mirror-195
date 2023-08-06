# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ververser',
 'ververser.examples.1_minimal_setup',
 'ververser.examples.1_minimal_setup.content',
 'ververser.examples.2_game_class',
 'ververser.examples.2_game_class.content',
 'ververser.examples.3_reloading_script_imports',
 'ververser.examples.3_reloading_script_imports.content']

package_data = \
{'': ['*']}

install_requires = \
['pyglet>=2.0.5,<3.0.0']

setup_kwargs = {
    'name': 'ververser',
    'version': '0.1.14',
    'description': 'A lightweight wrapper around pyglet that allows hot-reloading of content.',
    'long_description': 'None',
    'author': 'Berry van Someren',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
