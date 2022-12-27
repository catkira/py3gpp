[![Python package](https://github.com/catkira/py3gpp/actions/workflows/python-package.yml/badge.svg)](https://github.com/catkira/py3gpp/actions/workflows/python-package.yml)
[![Pylint](https://catkira.github.io/py3gpp/pylint.svg)](https://github.com/catkira/py3gpp/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/py3gpp.svg)](https://badge.fury.io/py/py3gpp)
[![Downloads](https://pepy.tech/badge/py3gpp)](https://pepy.tech/project/py3gpp)

# Summary
This python package aims to replace the Matlab 5G Toolbox in Python. The call syntax of functions is the same as in matlab where possible. There are some differences, because matlab allows to continuously index a multidimensional array in one axis. In python this is not possible, therefore the result of functions like nrPBCHIndices() is also multidimensional here to make it compatible with Python.

# Installation
'python3 -m pip install py3gpp'
or
clone this repo and then do 'python3 -m pip install -e .'

# Getting started
run 'examples/test_py3gpp.ipynb'

The example data is ideal data generated with Matlab, but the code has been tested with real data that has CFO, SFO and noise.

# Documentation
See Matlab documentation of equivalent function
