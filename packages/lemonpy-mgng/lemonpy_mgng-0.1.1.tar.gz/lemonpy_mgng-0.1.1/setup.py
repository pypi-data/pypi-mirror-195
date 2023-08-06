# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lemonpy_mgng']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0', 'numpy>=1.18.1,<2.0.0']

setup_kwargs = {
    'name': 'lemonpy-mgng',
    'version': '0.1.1',
    'description': 'mgng',
    'long_description': '# Welcome to mgng\n\nAn experimental implementation of the Merge Growing Neural Gas algorithm.\nThe project turned into an exercise for using state-of-the-art python tools.\nThis project has been created with my [cookiecutter for science projects](https://bitbucket.org/StefanUlbrich/science-cookiecutter/src/master/)\n\n## The Growing Neural Gas and Merge Growing Neural Gas Algorithms\n\n[*Growing Neural Gas (NGN)*](https://papers.nips.cc/paper/893-a-growing-neural-gas-network-learns-topologies.pdf) is a [topology preserving (see this blog for a demonstration)](http://neupy.com/2018/03/26/making_art_with_growing_neural_gas.html) or [this explaination](http://neupy.com/2018/03/26/making_art_with_growing_neural_gas.html#id1)) extension to the [*Neural gas (NG)*]() approach is usefull for learning when an underlying topology is not known (as in the case of the [*Self-organizing maps (SOM)*]() algorithm). When it comes to time series data (such as trajectories), an extension to the neural gas algorithm has been approached (*Merge Neural Gas (MNG)*) and a combination with the GNG leads to the [*Merge growing neural gas (MNGN)*](https://ias.in.tum.de/_media/spezial/bib/andreakis09wsom.pdf) approach. It adds a context memory to the neurons of the NGN and is useful for *recognising* temporal sequences and with a single weighting parameter, can be reduced to a regular NGN for which an implementation [is available](https://github.com/itdxer/neupy/blob/master/notebooks/growing-neural-gas/Making%20Art%20with%20Growing%20Neural%20Gas.ipynb).\n\nThis packages implements the MGNG algorithm as a vanilla [numpy](https://numpy.org/) implementation (which can be executed on the GPU with [Cupy](https://cupy.chainer.org/)). The package uses modern python tools such as [poetry](https://python-poetry.org/), [attrs](https://www.attrs.org/en/stable/) (a focus has been laid on those two for this release), and sphinx and mypy/pylint/black for documentation and coding standards.\n\nSee the notebooks in the repective subfolder of the project root and the [documentation](https://stefanulbrich.github.io/MergeGNG/api/mgng.mgng.html).\n\n## Installation and development\n\nFirst make sure to install Python (^3.7) the dependency management\ntool [Poetry](https://python-poetry.org/) then create an isolated virtual\nenvironment and install the dependencies:\n\n```sh\npoetry install\n```\n\nPer terminal session,  the following command should be executed\nto activate the virtual environment.\n\n```sh\npoetry shell\n```\n\nTo generate the documentation run:\n\n```sh\ncd doc/\nmake api # optional, only when the code base changes\nmake html\n```\n\nTo run unit tests, run:\n\n```sh\npytest --log-level=WARNING\n# Specify a selected test\npytest --log-level=DEBUG -k "TestExample"\npytest --log-level=DEBUG tests/test_example.py::TestExample::test_example\n```\n\nTo work with [VisualStudio Code](https://code.visualstudio.com/):\n\n```sh\ncp .vscode/template.settings.json .vscode/settings.json\nwhich python # copy the path without the executable\n```\n\nand add the path to the virtual environment to in the `"python.pythonPath"` setting.\n\n```sh\ncp .vscode/template.settings.json .vscode/settings.json\nwhich python # copy the path without the executable\n```\n\nand add the path to the virtual environment to in the `"python.pythonPath"` setting.\n',
    'author': 'Stefan Ulbrich',
    'author_email': '6009224+stefanulbric@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
