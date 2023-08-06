# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['velovi']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.7.5',
 'scikit-learn>=0.21.2',
 'scvelo>=0.2.5',
 'scvi-tools>=0.20.1']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'dev': ['black>=20.8b1',
         'codecov>=2.0.8',
         'ruff',
         'jupyter>=1.0',
         'pre-commit>=2.7.1',
         'pytest>=4.4',
         'pytest-cov',
         'scanpy>=1.6'],
 'docs': ['ipython>=7.1.1',
          'ipython>=7.1.1',
          'sphinx-book-theme>=1.0.0',
          'myst-nb',
          'sphinx-copybutton',
          'sphinxcontrib-bibtex',
          'ipykernel',
          'scanpydoc>=0.5',
          'sphinx>=4.1',
          'sphinx-autodoc-typehints'],
 'tutorials': ['scanpy>=1.6']}

setup_kwargs = {
    'name': 'velovi',
    'version': '0.2.0',
    'description': 'Estimation of RNA velocity with variational inference.',
    'long_description': "# velovi\n\n[![Tests][badge-tests]][link-tests]\n[![Documentation][badge-docs]][link-docs]\n\n[badge-tests]: https://img.shields.io/github/actions/workflow/status/yoseflab/velovi/test.yml?branch=main\n[link-tests]: https://github.com/yoseflab/velovi/actions/workflows/test.yml\n[badge-docs]: https://img.shields.io/readthedocs/velovi\n\nVariational inference for RNA velocity. This is an experimental repo for the veloVI model. Installation instructions and tutorials are in the docs. Over the next few months veloVI will move into [scvelo](https://scvelo.org/).\n\n## Getting started\n\nPlease refer to the [documentation][link-docs].\n\n## Installation\n\nYou need to have Python 3.8 or newer installed on your system. If you don't have\nPython installed, we recommend installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html).\n\nThere are several alternative options to install velovi:\n\n<!--\n1) Install the latest release of `velovi` from `PyPI <https://pypi.org/project/velovi/>`_:\n\n```bash\npip install velovi\n```\n-->\n\n1. Install the latest release on PyPI:\n\n```bash\npip install velovi\n```\n\n2. Install the latest development version:\n\n```bash\npip install git+https://github.com/yoseflab/velovi.git@main\n```\n\n## Release notes\n\nSee the [changelog][changelog].\n\n## Contact\n\nFor questions and help requests, you can reach out in the [scverse discourse][scverse-discourse].\nIf you found a bug, please use the [issue tracker][issue-tracker].\n\n## Citation\n\n```\n@article{gayoso2022deep,\n  title={Deep generative modeling of transcriptional dynamics for RNA velocity analysis in single cells},\n  author={Gayoso, Adam and Weiler, Philipp and Lotfollahi, Mohammad and Klein, Dominik and Hong, Justin and Streets, Aaron M and Theis, Fabian J and Yosef, Nir},\n  journal={bioRxiv},\n  pages={2022--08},\n  year={2022},\n  publisher={Cold Spring Harbor Laboratory}\n}\n```\n\n[scverse-discourse]: https://discourse.scverse.org/\n[issue-tracker]: https://github.com/yoseflab/velovi/issues\n[changelog]: https://velovi.readthedocs.io/latest/changelog.html\n[link-docs]: https://velovi.readthedocs.io\n[link-api]: https://velovi.readthedocs.io/latest/api.html\n",
    'author': 'Adam Gayoso',
    'author_email': 'adamgayoso@berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YosefLab/velovi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
