import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrPDSCH import nrPDSCH

def run_nr_pdsch(cws, modulation, nlayers, nid, nrnti, eng):
    ref_data = eng.nrPDSCH(cws, modulation, matlab.double(nlayers), matlab.double(nid),  matlab.double(nrnti), nargout=1)
    ref_data = np.array(list(itertools.chain(*ref_data)))
    ref_data = np.around(ref_data, 4)

    data = nrPDSCH( [np.array(list(itertools.chain(*cws)), dtype=(int))], modulation, nlayers, nid, nrnti )
    data = np.around(data, 4)

    assert np.all(ref_data == data)

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("modulation", [["256QAM"], ["64QAM"], ["16QAM"], ["QPSK"]])
@pytest.mark.parametrize("nlayers", [1])
@pytest.mark.parametrize("nid", [0, 1])
@pytest.mark.parametrize("nrnti", [0, 1])
def test_run_nr_pdsch(modulation, nlayers, nid, nrnti, eng):
    databits = eng.randi(matlab.double([0, 1]), 4800, 1)
    run_nr_pdsch(databits, modulation, nlayers, nid, nrnti, eng)

if __name__ == '__main__':
    test_run_nr_pdsch(["64QAM"], 1, 0, 0)