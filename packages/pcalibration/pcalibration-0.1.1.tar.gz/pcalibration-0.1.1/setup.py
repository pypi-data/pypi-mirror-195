# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcalibration']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0', 'scikit-learn>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'pcalibration',
    'version': '0.1.1',
    'description': '',
    'long_description': '# probability-calibration',
    'author': 'nutorbit',
    'author_email': 'nutorbitx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
