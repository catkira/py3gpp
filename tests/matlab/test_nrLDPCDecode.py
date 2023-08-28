import matlab.engine
import numpy as np
import pytest
from py3gpp.nrLDPCDecode import nrLDPCDecode

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("K", [2560])
@pytest.mark.parametrize("C", [1, 2, 3])
@pytest.mark.parametrize("F", [36])
@pytest.mark.parametrize("bgn", [2])
@pytest.mark.parametrize("vectorize", [True, False])
def test_nrLDPCDecode(K, C, F, bgn, vectorize, eng):
    # cbs = np.ones((K - F, C))
    cbs = np.random.randint(2, size = (K - F, C))
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    txcodedcbs = eng.nrLDPCEncode(eng.double(cbs), eng.double(bgn))
    txcodedcbs = np.asarray(txcodedcbs)

    fill_indices = (txcodedcbs[:, 0] == -1)

    # convert to rx soft bits
    rxcodedcbs = (1 - 2 * txcodedcbs.astype(np.double))

    rxcodedcbs[fill_indices, :] = 0

    [rxcbs, actualniters] = nrLDPCDecode(rxcodedcbs.copy(), bgn, 20, vectorize = vectorize)
    np.array_equal(rxcbs, cbs)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    bgn = 2
    C = 2
    K = 2560
    F = 36
    test_nrLDPCDecode(K, C, F, bgn, 0, _eng)
    _eng.quit()