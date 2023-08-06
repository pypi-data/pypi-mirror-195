# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.visualization']

package_data = \
{'': ['*'], 'src.visualization': ['assets/*']}

install_requires = \
['dash-bio>=1.0.2,<2.0.0',
 'dash-bootstrap-components>=1.3.0,<2.0.0',
 'dash>=2.6.1,<3.0.0',
 'h5py>=3.7.0,<4.0.0',
 'kaleido==0.2.1',
 'llvmlite>=0.39.1,<0.40.0',
 'matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pyfaidx>=0.7.1,<0.8.0',
 'pyyaml>=6.0,<7.0',
 'seaborn>=0.12.0,<0.13.0',
 'umap-learn>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['rostspace = src.app:main']}

setup_kwargs = {
    'name': 'rostspace',
    'version': '0.1.0',
    'description': 'Protein Embedding Visualization Tool.',
    'long_description': '# ProtSpace3D\n\nThis is a bachelor thesis project, \nDevelopment of protein-embedding visualization tool.\n\n## Installing dependencies\n\nPython-poetry(https://python-poetry.org/) is used for installing the dependencies. Follow the instruction \non the website to install poetry.\nAfter that run\n\n```shell\npoetry install\n```\n\nto install the dependencies for this project.\n\n## Running the script\n\nThe script to be executed is processing.py with the arguments:\n\n    ->  -d          Name of the folder which holds the required data, .h5 .csv & .fasta (String)\n    ->  -b          Name of the files which are in the data folder, requires equal names (String)\n    ->  --sep       The character which seperates the columns in the .csv file (Character)\n    ->  --uid_col   The column number which holds the unique ID, starting from 0 (Integer)\n    ->  --html_cols If set, html file(s) of the selected column(s) is saved in data directory, starting from 1 ignoring the uid_col (Integer)\n    ->  --pdb       Name of the directory in the data directory, which holds the .pdb files for viewing the molecule (String)\n\nExample:\n\n```shell\npoetry run python app.py -d data/ex1 -b VA\n```\n\nor with molecule visualization\n\n```shell\npoetry run python protspace3d/app.py -b Conotoxins_try1_mapped -d data/ex3 --pdb pdb\n```\n',
    'author': 'Anton Spannagl',
    'author_email': 'None',
    'maintainer': 'Rostlab',
    'maintainer_email': 'admin@rostlab.org',
    'url': 'https://github.com/Rostlab/RostSpace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
