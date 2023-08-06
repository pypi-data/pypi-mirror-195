# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bib2yaml']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'bibtexparser>=1.4.0,<2.0.0',
 'pylatexenc>=2.10,<3.0']

setup_kwargs = {
    'name': 'bib2yaml',
    'version': '1.0.0',
    'description': 'Converts a BibTeX file to YAML format',
    'long_description': "### Converts a BibTeX file to YAML format\n\nBIB2YAML is a lightweight Python package that provides an easy and efficient way to convert BibTeX (.bib) files to YAML (.yaml) format.\n\n### Usage\n\n```python\n\n    # interactive\n    # path to the bib file\n    bib = '/Users/aj/Downloads/ref.bib'\n    # path to the output directory\n    outputDir = '/Users/aj/Downloads/'\n    \n    # Run the function\n    bib2yaml (bib, outputDir, fileName='ref')\n    \n    # commandline\n    python bib2yaml.py --bib /Users/aj/Downloads/ref.bib --outputDir /Users/aj/Downloads/\n    \n\n```",
    'author': 'Ajit Johnson Nirmal',
    'author_email': 'ajitjohnson.n@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
