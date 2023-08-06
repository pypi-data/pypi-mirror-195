# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farcaster_cli']

package_data = \
{'': ['*']}

install_requires = \
['farcaster>=0.7.2,<0.8.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['farcaster-cli = farcaster_cli.main:start']}

setup_kwargs = {
    'name': 'farcaster-cli',
    'version': '0.1.0',
    'description': 'Farcaster CLI Client',
    'long_description': '---\ntitle: Farcaster CLI Client\ndescription: A Farcaster CLI Client written in Python\ntags:\n  - python\n  - Farcaster\n---\n## ✨ Features\n\n- Read casts from everyone\n- Read casts from the people you follow\n\n## 💁\u200d♀️ How to use\n\n- Install package using `poetry add farcaster-cli`\n- Start the bot using `poetry run python main.py`\n',
    'author': 'Mason Hall',
    'author_email': 'masonhall@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
