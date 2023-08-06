# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configloaders']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'configloaders',
    'version': '0.4.9',
    'description': 'Load configurations from a variety of configuration files and use them easily',
    'long_description': 'Load configurations from a variety of configuration files and use them easily\n\n# Examples\n\n## Load configuration file if it exists\n\n```python\nimport configloaders\n\nusername = \'username\'\npassword = \'password\'\nphone = 123456789\nauto_login = True\n\nconfigloaders.load_json(globals())\n```\n\n## Load the configuration and update it on exit\n\n```python\nimport configloaders\n\nusername = \'username\'\npassword = \'password\'\nphone = 123456789\nauto_login = True\n\nconfigloaders.load_json(globals(), save_on_exit=True)\n```\n\n## Load the configuration and require the configuration file to exist\n\n```python\nimport configloaders\n\nusername = \'username\'\npassword = \'password\'\nphone = 123456789\nauto_login = True\n\nconfigloaders.load_json(globals(), required=True)\n```\n\n## Manually save the configuration\n\n```python\nimport configloaders\n\nusername = \'username\'\npassword = \'password\'\nphone = 123456789\nauto_login = True\n\nconfigloaders.load_json(globals()).dump()\nconfigloaders.load_json(globals()).dump(original=True)\nconfigloaders.dump()\nconfigloaders.dump(original=True)\n```\n\n## Take all configuration items as command line arguments\n\n```python\nimport configloaders\n\nusername = \'username\'\npassword = \'password\'\nphone = 123456789\nauto_login = True\n\nconfigloaders.load_argparse(globals())\n# or\nimport argparse\nparser = argparse.ArgumentParser()\nconfigloaders.load_argparse(globals(), parser)\nparser.parse_args()\n```\n\n# Features\n\n* Variables of the module type and those prefixed with "__" are ignored',
    'author': 'jawide',
    'author_email': 'jawide@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
