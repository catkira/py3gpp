import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrPSS import nrPSS
from py3gpp.nrPSSIndices import nrPSSIndices

def run_nr_pss(ncellid, eng):
    ref_data = eng.nrPSS(matlab.double(ncellid))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    ref_ind = eng.nrPSSIndices()
    ref_ind = np.array(list(itertools.chain(*ref_ind)))
    ref_ind = np.array(ref_ind - 1)

    data = nrPSS(ncellid)
    indices = nrPSSIndices()

    assert np.all(ref_data == data)
    assert np.all(indices == ref_ind)

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("ncellid", [0, 1, 2, 3, 207, 209, 500, 1007])
def test_nr_pss(ncellid, eng):
    run_nr_pss(ncellid, eng)
