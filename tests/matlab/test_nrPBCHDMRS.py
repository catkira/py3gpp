import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrPBCHDMRS import nrPBCHDMRS
from py3gpp.nrPBCHDMRSIndices import nrPBCHDMRSIndices

def run_nr_pbch_dmrs(ncellid, issb, eng):
    ref_data = eng.nrPBCHDMRS(matlab.double(ncellid), matlab.double(issb))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    ref_ind = eng.nrPBCHDMRSIndices(matlab.double(ncellid))
    ref_ind = np.array(list(itertools.chain(*ref_ind)))
    ref_ind = np.array(ref_ind - 1)

    data = nrPBCHDMRS(ncellid, issb)
    indices = nrPBCHDMRSIndices(ncellid)

    ref_data = np.around(ref_data, 4)
    data = np.around(data, 4)

    assert np.all(ref_data == data)
    assert np.all(ref_ind == indices)

@pytest.mark.parametrize("ncellid", [0, 500, 1007])
@pytest.mark.parametrize("issb", list(range(8)))
def test_nr_pbch_dmrs(ncellid, issb):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_pbch_dmrs(ncellid, issb, eng)
    finally:
        eng.quit()
