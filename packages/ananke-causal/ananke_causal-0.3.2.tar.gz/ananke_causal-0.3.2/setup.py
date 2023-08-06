# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ananke',
 'ananke.datasets',
 'ananke.datasets.simulated',
 'ananke.discovery',
 'ananke.estimation',
 'ananke.graphs',
 'ananke.identification',
 'ananke.models']

package_data = \
{'': ['*'], 'ananke.datasets': ['real/*']}

install_requires = \
['numpy>=1.23.0,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pgmpy>=0.1.21,<0.2.0',
 'scipy>=1.8.1,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0']

extras_require = \
{'viz': ['pygraphviz', 'graphviz>=0.20.1,<0.21.0']}

setup_kwargs = {
    'name': 'ananke-causal',
    'version': '0.3.2',
    'description': 'Ananke, named for the Greek primordial goddess of necessity and causality, is a python package for causal inference using the language of graphical models.',
    'long_description': '# Ananke\n\nVisit the [website](https://ananke.readthedocs.io) to find out more.\n\n[Ananke](https://en.wikipedia.org/wiki/Ananke), named for the Greek\nprimordial goddess of necessity and causality, is a python package for\ncausal inference using the language of graphical models\n\n## Contributors\n\n* Rohit Bhattacharya \n* Jaron Lee\n* Razieh Nabi \n* Preethi Prakash\n* Ranjani Srinivasan\n\nInterested contributors should check out the [CONTRIBUTING.md](CONTRIBUTING.md) for further details.\n\n## Installation\n\nIf graph visualization is not required then install via `pip`:\n\n```\npip install ananke-causal\n```\n\nAlternatively, the package may be installed from gitlab by cloning and `cd` into the directory. Then, `poetry` (see https://python-poetry.org) can be used to install:\n\n```\npoetry install\n```\n\n### Install with graph visualization\n\n\nIf graphing support is required, it is necessary to install [graphviz](https://www.graphviz.org/download/).\n\n\n#### Non M1 Mac instructions\nUbuntu:\n```shell script\nsudo apt install graphviz libgraphviz-dev pkg-config\n```\n\nMac ([Homebrew](https://brew.sh/)):\n```shell script\nbrew install graphviz\n```\n\nFedora:\n```shell script\nsudo yum install graphviz\n```\n\nOnce graphviz has been installed, then:\n\n```shell script\npip install ananke-causal[viz] # if pip is preferred\n\npoetry install --extras viz # if poetry is preferred\n```\n\n#### M1 Mac specific instructions\n\nIf on M1 see this [issue](https://github.com/pygraphviz/pygraphviz/issues/398). The fix is to run the following before installing:\n```shell script\nbrew install graphviz\npython -m pip install \\\n    --global-option=build_ext \\\n    --global-option="-I$(brew --prefix graphviz)/include/" \\\n    --global-option="-L$(brew --prefix graphviz)/lib/" \\\n    pygraphviz\n```\n',
    'author': 'Ananke community',
    'author_email': 'rbhatta8@jhu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/causal/ananke',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
