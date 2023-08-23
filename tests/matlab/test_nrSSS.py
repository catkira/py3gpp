import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrSSS import nrSSS
from py3gpp.nrSSSIndices import nrSSSIndices

def run_nr_sss(ncellid, eng):
    ref_data = eng.nrSSS(matlab.double(ncellid))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    ref_ind = eng.nrSSSIndices()
    ref_ind = np.array(list(itertools.chain(*ref_ind)))
    ref_ind = np.array(ref_ind - 1)

    data = nrSSS(ncellid)
    indices = nrSSSIndices()

    assert (ref_data == data).all()
    assert (indices == ref_ind).all()

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("ncellid", [0, 600, 1007])
def test_nr_sss(ncellid, eng):
    run_nr_sss(ncellid, eng)

