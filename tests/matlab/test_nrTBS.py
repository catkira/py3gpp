import matlab.engine
import numpy as np
import pytest
from py3gpp.nrTBS import nrTBS

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("modulation", [['QPSK', '64QAM']])
@pytest.mark.parametrize("nlayers", [4, 8])
@pytest.mark.parametrize("nPRB", [25, 106])
@pytest.mark.parametrize("NREPerPRB", [100])
@pytest.mark.parametrize("tcr", [[0.3701, 0.4277]])
@pytest.mark.parametrize("xOh", [0])
@pytest.mark.parametrize("tbScaling", [1])
def test_nrTBS(modulation, nlayers, nPRB, NREPerPRB, tcr, xOh, tbScaling, eng):
    tb_two_cw = nrTBS(modulation, nlayers, nPRB, NREPerPRB, tcr, xOh, tbScaling)
    tb_two_cw_ref = np.asarray(eng.nrTBS(modulation, nlayers, nPRB, NREPerPRB, eng.double(np.array(tcr)), xOh, eng.double(tbScaling))).astype(int)[0]
    assert np.array_equal(tb_two_cw, tb_two_cw_ref)


if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    # Test for two codewords
    modulation = ['QPSK', '64QAM']
    nlayers = 8
    nPRB = 106
    NREPerPRB = 100
    tcr = [0.3701, 0.4277]
    xOh = 0
    tbScaling = 1
    test_nrTBS(modulation, nlayers, nPRB, NREPerPRB, tcr, xOh, tbScaling, _eng)
    _eng.quit()