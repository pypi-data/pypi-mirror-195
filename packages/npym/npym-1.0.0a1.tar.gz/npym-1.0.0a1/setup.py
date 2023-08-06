# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npym']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'npym',
    'version': '1.0.0a1',
    'description': 'Support package for NPyM, to install NPM packages with Python package managers.',
    'long_description': '# NPyM\n\nNPyM is a service that translates NPM packages into Python wheels so that you\ncan install them using a Python package manager. This helps calling JS code\nfrom Python, especially if you combine it with\n[Node Edge](https://node-edge.readthedocs.io/en/latest/).\n\nThis package is a support package for NPyM, which is depended upon by the\nconverted NPM packages.\n\nIt provides:\n\n- A wrapper to allow JS bin to be installed by package managers\n- A way to know where the `node_modules` is installed\n\nIn order to know this, you can easily do:\n\n```python\nfrom npym import node_modules\n\nprint(node_modules)\n```\n',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
