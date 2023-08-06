# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['linkml_transformer',
 'linkml_transformer.cli',
 'linkml_transformer.compiler',
 'linkml_transformer.datamodel',
 'linkml_transformer.importer',
 'linkml_transformer.schema_mapper',
 'linkml_transformer.transformer',
 'linkml_transformer.utils']

package_data = \
{'': ['*']}

install_requires = \
['linkml-runtime>=1.4.5,<2.0.0']

entry_points = \
{'console_scripts': ['linkml-tr = linkml_transformer.cli.cli:main']}

setup_kwargs = {
    'name': 'linkml-transformer',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'cmungall',
    'author_email': 'cjm@berkeleybop.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
