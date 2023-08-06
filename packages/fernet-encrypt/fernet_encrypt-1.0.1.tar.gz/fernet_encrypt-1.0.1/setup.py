# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'pysrc'}

packages = \
['fernet_encrypt']

package_data = \
{'': ['*'], 'fernet_encrypt': ['keys/.gitignore']}

install_requires = \
['cryptography>=39.0.2,<40.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['fernet-encrypt = fernet_encrypt:cli']}

setup_kwargs = {
    'name': 'fernet-encrypt',
    'version': '1.0.1',
    'description': 'Fernet Encryption CLI tool',
    'long_description': '# Fernet Encryption CLI tool\n\n## Install\nUse [pipx](https://pypa.github.io/pipx/) to install globally in an isolated python environment.\n```bash\npipx install fernet-encrypt\n```\n\n## Usage\n```\nCommands:\n  create-fernet-key\n  encrypt-file\n  decrypt-file\n```\n\n### create-fernet-key\nCreate a new fernet key to sign with. Keys will be stored in fernet-encrypt install location. When decrypting, all available keys will be tried until one succeeds or they are all exhasted.\n```\nUsage: fernet-encrypt create-fernet-key [OPTIONS]\n\nOptions:\n  --help  Show this message and exit.\n```\n\n### encrypt-file\nEncrypt provided `INPUT_FILE` with the newest fernet key (see `create-fernet-key`). The encrypted output will be directed to `OUTPUT_FILE` if provided. Otherwise output will be directed to stdout.\n```\nUsage: fernet-encrypt encrypt-file [OPTIONS] INPUT_FILE\n                                   [OUTPUT_FILE]\n\nArguments:\n  INPUT_FILE     [required]\n  [OUTPUT_FILE]\n\nOptions:\n  --help  Show this message and exit.\n  ```\n\n### decrypt-file\nDecrypt provided `INPUT_FILE`. All existing fernet keys will be used for decryption until one succeeds or they are all exhasted. The decrypted output will be directed to `OUTPUT_FILE` if provided. Otherwise output will be directed to stdout.\n```\nfernet-encrypt decrypt-file [OPTIONS] INPUT_FILE\n                            [OUTPUT_FILE]\n\nArguments:\n  INPUT_FILE     [required]\n  [OUTPUT_FILE]\n\nOptions:\n  --help  Show this message and exit.\n  ```\n',
    'author': 'Tyson Holub',
    'author_email': 'tyson@tysonholub.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
