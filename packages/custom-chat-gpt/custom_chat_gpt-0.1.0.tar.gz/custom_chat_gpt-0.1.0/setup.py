# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chat_gpt']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.0,<0.28.0', 'rich>=13.3,<14.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['chat-gpt = chat_gpt.main:app']}

setup_kwargs = {
    'name': 'custom-chat-gpt',
    'version': '0.1.0',
    'description': 'Use chapgpt from your terminal',
    'long_description': 'poetry init\npoetry add openai rich \npoetry shell\npoetry install\npoetry run python script.py',
    'author': 'RomainEconomics',
    'author_email': 'jouhameau.romain@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
