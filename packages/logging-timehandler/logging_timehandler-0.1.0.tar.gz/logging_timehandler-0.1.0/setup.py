# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging_timehandler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logging-timehandler',
    'version': '0.1.0',
    'description': '',
    'long_description': "Log files are generated based on the time and the latest n logs are automatically retained\n\n# Example\n\n```python\nimport logging\nimport logging_timehandler\n\nlogger = logging.getLogger(__name__)\nhandler = logging_timehandler.TimeHandler('./log/%Y_%m_%d/%Y_%m_%d_%S.txt', retain=5)\nhandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))\nlogger.addHandler(handler)\nlogger.setLevel(logging.INFO)\n\nfor i in range(10):\n    logger.info('hello')\n```",
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
