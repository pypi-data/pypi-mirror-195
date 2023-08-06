# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lemonpy']

package_data = \
{'': ['*']}

extras_require = \
{'dbc': ['design-by-contract>=0.3.1,<0.4.0'],
 'mgng': ['lemonpy-mgng>=0.1.1,<0.2.0']}

setup_kwargs = {
    'name': 'lemonpy',
    'version': '0.0.3',
    'description': 'A meta package for projects revolving around kinematics configuration solving and self-organization in machine learning',
    'long_description': '# Welcome to Lemonpy\n\nThis is a meta packages for my research about geometric approaches to solving kinematics projects and machine learning related topics. Visit my blog at [lemonfold.io](https://lemonfold.io).\n\nInstall with \n\n```sh\npoetry install -E "dbc mgng"\n```\n\nWhere the extras install the following packages\n\n* **dbc**: [design-by-contract]()–A design-by-contract Library\n* **mgng**: [lemonpy-mgng](https://github.com/StefanUlbrich/MergeGNG)–An implementation of the merge growing neural gas algorithm\n  ',
    'author': 'Stefan Ulbrich',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/StefanUlbrich/lemonpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
