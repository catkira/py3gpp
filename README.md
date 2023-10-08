[![CI](https://github.com/catkira/py3gpp/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/catkira/py3gpp/actions/workflows/lint_and_test.yml)
[![Pylint](https://catkira.github.io/py3gpp/pylint.svg)](https://github.com/catkira/py3gpp/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/py3gpp.svg)](https://badge.fury.io/py/py3gpp)
[![Downloads](https://static.pepy.tech/badge/py3gpp)](https://pepy.tech/project/py3gpp)

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

# Coding Guideline
## Formatting
* Screen width 120
* spaces on each side of math operators like +-*/
* run `pre-commit run -a` before any push. Otherwise PR will be rejected
## Testing
* Each function must have a hard-coded test that can run on CI
* Each function should have a Matlab test that can run on a machine with Matlab license
* Hard-coded test cases should cover the most common argument combinations
* Matlab tests should cover more argument combinations than the hard-coded tests
## Function interface
* Functions should return numpy arrays if the return value is an array
* Functions should accept numpy arrays and python lists if an input value is an array
* Config objects should have a getter and setter method and declare the internal variable with underscore at the beginning
* Input arguments should be checked and a 'ValueError' or 'TypeError' should be raised if an argument is not correct
