import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrPRBS import nrPRBS

def run_nr_prbs(cinit, size, eng):
    ref_data = eng.nrPRBS(matlab.double(cinit), matlab.double(size))
    ref_data = list(itertools.chain(*ref_data))
    ref_data = np.array([x*1 for x in ref_data])

    data = nrPRBS(cinit, size)

    assert np.all(ref_data == data)
    
@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("cinit", [0, 100, 1245345, 534667868])
@pytest.mark.parametrize("size", [1024, 8192])
def test_nr_prbs(cinit, size, eng):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_prbs(cinit, size, eng)
    finally:
        eng.quit()
