# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qq_picture_operation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qq-picture-operation',
    'version': '0.1.0',
    'description': '进行qq图片的操作，用来转移复制删除图片 进行qq图片的操作，用来转移复制删除图片',
    'long_description': '# QQ_picture_operation\n 进行qq图片的操作，用来转移复制删除图片\n',
    'author': 'ziru-w',
    'author_email': '77319678+ziru-w@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
