import matlab.engine
import numpy as np
import pytest
from py3gpp.nrLDPCEncode import nrLDPCEncode

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("K", [2560])
@pytest.mark.parametrize("C", [1, 2, 3])
@pytest.mark.parametrize("F", [36])
@pytest.mark.parametrize("bgn", [2])
def test_nrLDPCEncode(K, C, F, bgn, eng):
    # cbs = np.ones((K - F, C))
    cbs = np.random.randint(2, size = (K - F, C))
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    codedcbs_ref = eng.nrLDPCEncode(eng.double(cbs), eng.double(bgn))
    codedcbs_ref = np.asarray(codedcbs_ref)
    codedcbs = nrLDPCEncode(cbs, bgn)
    assert codedcbs_ref.shape == codedcbs.shape
    assert np.array_equal(codedcbs, codedcbs_ref)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    bgn = 2
    C = 2
    K = 2560
    F = 36
    test_nrLDPCEncode(K, C, F, bgn, _eng)
    _eng.quit()