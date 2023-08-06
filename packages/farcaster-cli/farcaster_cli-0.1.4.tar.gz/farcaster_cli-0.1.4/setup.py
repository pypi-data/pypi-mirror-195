# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farcaster_cli']

package_data = \
{'': ['*']}

install_requires = \
['farcaster>=0.7.3,<0.8.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['farcaster-cli = farcaster_cli.main:start']}

setup_kwargs = {
    'name': 'farcaster-cli',
    'version': '0.1.4',
    'description': 'Farcaster CLI Client',
    'long_description': '# farcaster-cli\n\n<div align="center">\n\n[![Python Version](https://img.shields.io/pypi/pyversions/farcaster-cli.svg)](https://pypi.org/project/farcaster-cli/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![chat](https://img.shields.io/badge/chat-telegram-blue)](https://t.me/+aW_ucWeBVUZiNThh)\n\nfarcaster-cli is a CLI client for the Farcaster protocol<br></br>\n\n</div>\n\n## Installation\n\n```bash\npip install farcaster-cli\n```\n\nor install with [Poetry](https://python-poetry.org/):\n\n```bash\npoetry add farcaster-cli\n```\n\n## Usage\n\nThis client leverages the Warpcast API. [Warpcast](https://warpcast.com/) is one of many Farcaster [clients](https://github.com/a16z/awesome-farcaster#clients). As more APIs are created and hosted by different clients, these will be added to the CLI.\n\nTo use the Warpcast API you need to have a Farcaster account. We will use the mnemonic or private key of the Farcaster custody account (not your main wallet) to connect to the API.\n\nFirst, save your Farcaster mnemonic or private key to a $MNEMONIC environment variable. Now you can initialize the client, and automatically connect.\n\n\n```bash\nexport MNEMONIC = <your custody seed phrase here>\n```\n\n```bash\nfarcaster-cli $MNEMONIC --watch-all\n```\n\nThis subscribes to all recent casts. If you want only the casts of people you follow, remove `--watch-all`.\nYou can also include `--skip-existing` to only get new casts after the client starts.',
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
