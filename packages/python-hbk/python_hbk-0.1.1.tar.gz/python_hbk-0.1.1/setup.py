# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_hbk']

package_data = \
{'': ['*']}

install_requires = \
['aiofile>=3.8.1,<4.0.0', 'ujson>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'python-hbk',
    'version': '0.1.1',
    'description': 'Python tool to work with .hbk bookmark files from Hex Workshop',
    'long_description': '## How to use\n\n```python\nfrom python_hbk.Hbk import Hbk\n\nmy_hbk = Hbk(filepath="test.hbk")\nfor name, address, length in my_hbk.get_bookmarks():\n    print(f"{name=}, {address=}, {length=}")\n\nprint(my_hbk.to_json())\n```\n\n## Output\n```\nname=\'Test float\', address=\'0000016A\', length=4\nname=\'Test double\', address=\'0000016E\', length=8\nname=\'Test string\', address=\'00000176\', length=72\nname=\'Test float array [0]\', address=\'00000241\', length=4\n...\nname=\'Test double array [15]\', address=\'000002C7\', length=8\n\n[\n  {\n    "name": "Test float",\n    "address": "0000016A",\n    "length": 4\n  },\n  {\n    "name": "Test double",\n    "address": "0000016E",\n    "length": 8\n  },\n  {\n    "name": "Test string",\n    "address": "00000176",\n    "length": 72\n  },\n  {\n    "name": "Test float array [0]",\n    "address": "00000241",\n    "length": 4\n  },\n  ...\n  {\n    "name": "Test double array [15]",\n    "address": "000002C7",\n    "length": 8\n  }\n]\n\n```',
    'author': 'Sergey Rivov',
    'author_email': 'rvngtn@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Rivko/python-hbk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
