# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sncopy']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['sncopy = sncopy.cli:main']}

setup_kwargs = {
    'name': 'sncopy',
    'version': '0.1.0',
    'description': 'Copy-Paste Tool from Slack to Notion',
    'long_description': "# sncopy; Copy-Paste Tool from Slack to Notion\n\nIt's very stressfull to copy some contents on Slack to Notion because their html are not compatible.  \nSo, when I copy the contents include `Bulleted list` or `Numbered list`, I have to fix them manually.  \n\n## What is the difference\n\nThese are the sample outputs of copy from Slack and Notion.\nIn short, we will save text as plain text not markdown on Slack.\n\n**Case 1 : normal lines**\n\n```\n[Original]\nApple\nGoogle\nMicrosoft\n\n[on Slack]\n'Apple\\nGoogle\\nMicrosoft'\n\n[on Notion]\n'Apple\\n\\nGoogle\\n\\nMicrosoft'\n```\n\n**Case 2 : bulleted lines**\n\n```\n[Original]\n- Apple\n- Google\n  - Microsoft\n\n[on Slack]\n'Apple\\nGoogle\\nMicrosoft'\n\n[on Notion]\n'- Apple\\n- Google\\n    - Microsoft'\n```\n\n**Case 3 : numbered lines**\n\n```\n[Original]\n1. Apple\n2. Google\n  a. Microsoft\n\n[on Slack]\n'Apple\\nGoogle\\nMicrosoft'\n\n[on Notion]\n'1. Apple\\n1. Google\\n    1. Microsoft'\n```\n\nBecause Slack will return plain one, we cannot keep the structure of nested lines...  \n\n\n## Installation\n\n```\npip install sncopy\n```\n\n\n## Usage\n\nBasically, you only have to call `sncopy` on your terminal after copying your contents on Slack.  \nThis command will automatically convert them to Notion's format.  \n\nIf you want to convert to bulleted lines, please call `sncopy` command with `--mode` option.  \n\n```\nsncopy --mode bullet\n```\n\nfor numbered lines,  \n\n```\nsncopy --mode numbered\n```",
    'author': 'Kenichi Higuchi',
    'author_email': 'higuchi@adansons.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kenichihiguchi/sncopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
