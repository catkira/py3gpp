
import numpy as np
import pytest

from py3gpp.nrDLSCHInfo import nrDLSCHInfo

def run_nr_dlsch_info():
    R = 449/1024
    A = 50
    dlsch_info = nrDLSCHInfo(A, R)
    assert dlsch_info['F'] == 44

def test_run_nr_dlsch_info():
    run_nr_dlsch_info()

if __name__ == '__main__':
    run_nr_dlsch_info()