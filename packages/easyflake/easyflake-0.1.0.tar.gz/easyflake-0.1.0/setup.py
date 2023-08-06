# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyflake', 'easyflake.grpc', 'easyflake.node', 'easyflake.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'grpcio-health-checking>=1.51.3,<2.0.0',
 'grpcio>=1.51.3,<2.0.0',
 'lockfile>=0.12.2,<0.13.0']

extras_require = \
{':sys_platform == "linux" or sys_platform == "darwin"': ['python-daemon>=2.3.2,<3.0.0']}

entry_points = \
{'console_scripts': ['easyflake-cli = easyflake.__main__:cli']}

setup_kwargs = {
    'name': 'easyflake',
    'version': '0.1.0',
    'description': 'EasyFlake is a Python package for generating 64-bit IDs similar to Snowflake or Sonyflake.',
    'long_description': '# EasyFlake\n\n[![Test passing](https://github.com/tsuperis/easyflake/actions/workflows/test.yml/badge.svg)](https://github.com/tsuperis/easyflake/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/tsuperis/easyflake/branch/main/graph/badge.svg?token=3TIHGMYN1G)](https://codecov.io/gh/tsuperis/easyflake)\n![PyPI](https://img.shields.io/pypi/v/easyflake)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/easyflake)\n[![License](https://img.shields.io/github/license/tsuperis/easyflake)](https://github.com/tsuperis/easyflake/blob/main/LICENSE)\n\nEasyFlake is a Python package for generating 64-bit IDs similar to Snowflake or Sonyflake. It provides a simple way to generate unique and sortable IDs that can be used as primary keys in databases, message queue messages, or other distributed systems.\n\n## Installation\n\nInstall the latest version of EasyFlake using pip:\n\n```bash\npip install easyflake\n```\n\n## Usage\n\nTo use EasyFlake, simply create an instance of the `EasyFlake` class, passing in a unique node ID:\n\n```python\nfrom easyflake import EasyFlake\n\nef = EasyFlake(node_id=1)\nprint(ef.get_id())\n```\n\nThe `get_id()` method generates the next ID by the current timestamp. You can customize the number of bits used for the node ID and sequence ID parts, as well as the epoch timestamp and time scale.\n\n```python\nef = EasyFlake(node_id=0, node_id_bits=4, sequence_bits=6)\nprint(ef.get_id())\n```\n\n### Arguments\n\n* `node_id` (int): A unique ID for the current node. This ID should be between 0 and (2 ^ node_id_bits) - 1. If no argument is given, a random value is assigned to the node ID.\n* `node_id_bits` (int): The maximum number of bits used to represent the node ID. This argument defaults to 8 / max node ID is 255.\n* `sequence_bits` (int): The maximum number of bits used to represent the sequence number. This argument defaults to 8 / max sequence number is 255.\n* `epoch` (float): A timestamp used as a reference when generating the timestamp section of the ID. This argument defaults to 1675859040 (2023-02-08T12:24:00Z).\n* `time_scale` (int): The number of decimal places used to represent the timestamp. This argument defaults to 3 (milliseconds).\n\n## Contributing\n\nSee the [contributing guide](https://github.com/tsuperis/easyflake/blob/main/CONTRIBUTING.md).\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/tsuperis/easyflake/blob/main/LICENSE) file for details.\n',
    'author': 'Takeru Furuse',
    'author_email': 'tsuperis@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tsuperis/easyflake',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
