# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moana',
 'moana.corner',
 'moana.david_bennett_fit',
 'moana.dbc',
 'moana.external_format_io',
 'moana.viewer']

package_data = \
{'': ['*'], 'moana': ['stylelib/*']}

install_requires = \
['backports-strenum>=1.2.4,<2.0.0',
 'bokeh>=2.3.1,<3.0.0',
 'file-read-backwards>=2.0.0,<3.0.0',
 'matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.6.2,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'moana-golmschenk',
    'version': '0.1.3',
    'description': '',
    'long_description': 'None',
    'author': 'Greg Olmschenk',
    'author_email': 'golmschenk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
