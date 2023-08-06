# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrh', 'pyrh.models']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.12.7,<2023.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'pyotp>=2.8.0,<3.0.0',
 'python-dateutil>=2.8,<3.0',
 'pytz>=2022.7.1,<2023.0.0',
 'requests>=2.23,<3.0',
 'yarl>=1.4.2,<2.0.0']

extras_require = \
{'docs': ['autodocsumm>=0.2.9,<0.3.0',
          'sphinx>=5.3.0,<6.0.0',
          'sphinx-autodoc-typehints>=1.19.5,<2.0.0',
          'sphinx_rtd_theme>=1.1.1,<2.0.0'],
 'notebook': ['notebook>=6.0.3,<7.0.0', 'python-dotenv>=0.13.0,<0.14.0']}

setup_kwargs = {
    'name': 'pyrh',
    'version': '2.1.2',
    'description': 'Unofficial Robinhood Python API',
    'long_description': '.. image:: https://i.imgur.com/74CYw5g.png\n   :target: https://github.com/robinhood-unofficial/pyrh\n   :alt: robinhood-logo\n\n-------------------------------------------------------------\n\npyrh - Unofficial Robinhood API\n###############################\n\n.. image:: https://github.com/robinhood-unofficial/pyrh/workflows/build/badge.svg?branch=master&event=push\n   :target: https://github.com/robinhood-unofficial/pyrh/actions?query=workflow%3Abuild+branch%3Amaster\n   :alt: Build Status\n\n.. image:: https://codecov.io/gh/robinhood-unofficial/pyrh/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/robinhood-unofficial/pyrh\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/pyrh/badge/?version=latest\n   :target: https://pyrh.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/v/pyrh?style=plastic\n   :target: https://pypi.org/project/pyrh/\n   :alt: PyPI Version\n\n.. image:: https://img.shields.io/pypi/dm/pyrh?color=blue&style=plastic\n   :target: https://pypi.org/project/pyrh/\n   :alt: PyPI - Downloads\n\n.. image:: https://img.shields.io/github/license/robinhood-unofficial/Robinhood\n   :target: https://github.com/robinhood-unofficial/pyrh/blob/master/LICENSE\n   :alt: License\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Code Style\n\n.. image:: https://img.shields.io/gitter/room/J-Robinhood/Lobby\n   :target: https://gitter.im/J-Robinhood/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge\n   :alt: Gitter\n\nPython Framework to make trades with Unofficial Robinhood API. Supports Python 3.8.1+\n\n*Please note this project is not currently actively maintained, but is accepting contributions*\n\nDocumentation: https://pyrh.readthedocs.io/en/latest/\n\nQuick start\n***********\n\n.. code-block:: python\n\n   from pyrh import Robinhood\n\n   rh = Robinhood(username="YOUR_EMAIL", password="YOUR_PASSWORD")\n   rh.login()\n   rh.print_quote("AAPL")\n\nHow To Install:\n***************\n\n.. code-block::\n\n   pip install pyrh\n\nRunning example.ipynb_\n**********************\n\n.. _example.ipynb: https://github.com/robinhood-unofficial/pyrh/blob/master/notebooks/example.ipynb\n\nClone the repository and install jupyter capabilities.\n\n.. code-block::\n\n   $ git clone https://github.com/robinhood-unofficial/pyrh.git\n   $ cd pyrh\n   $ python --version # python 3.3+ for venv functionality\n   Python 3.8.1\n   $ python -m venv pyrh_env\n   $ source pyrh_env/bin/activate\n   (pyrh_env) $ pip install .[notebook]\n   (pyrh_env) $ cp .env.sample .env # update the values in here\n   (pyrh_env) $ jupyter notebook notebooks/example.ipynb\n\nNow just run the files in the example.\n\nRelated\n*******\n\n* `robinhood-ruby <https://github.com/rememberlenny/robinhood-ruby>`_ - RubyGem for interacting with Robinhood API\n* `robinhood-node <https://github.com/aurbano/robinhood-node>`_ - NodeJS module to make trades with Robinhood Private API\n* See the original `blog post <https://medium.com/@rohanpai25/reversing-robinhood-free-accessible-automated-stock-trading-f40fba1e7d8b>`_.\n',
    'author': 'Unofficial Robinhood Python API Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyrh.readthedocs.io/en/latest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
