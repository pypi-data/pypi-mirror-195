# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['common_fate_schema',
 'common_fate_schema.provider',
 'common_fate_schema.tests']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.5,<2.0.0']

setup_kwargs = {
    'name': 'common-fate-schema',
    'version': '0.1.0',
    'description': 'Common Fate core schema types',
    'long_description': '# common-fate-schema\n\nCore Common Fate schema type definitions.\n',
    'author': 'Common Fate',
    'author_email': 'hello@commonfate.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
