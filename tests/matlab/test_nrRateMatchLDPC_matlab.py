import matlab.engine
import numpy as np
import pytest
from py3gpp.nrRateMatchLDPC import nrRateMatchLDPC

def run_nrRateMatchLDPC(in_, outlen, rv, mod, nLayers, eng):
    ref_data = eng.nrRateMatchLDPC(eng.double(in_), eng.double(outlen), eng.double(rv), mod, eng.double(nLayers))
    ref_data = np.asarray(ref_data).ravel() # remove empty matlab axis
    out_data = nrRateMatchLDPC(in_, outlen, rv, mod, nLayers)
    assert np.array_equal(ref_data, out_data)

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("N", [3960])
@pytest.mark.parametrize("C", [1, 2, 3])
@pytest.mark.parametrize("rv", [0, 1, 2, 3])
@pytest.mark.parametrize("N_filler_bits", [0, 20])
def test_nrRateMatchLDPC_matlab(N, C, rv, N_filler_bits, eng):
    mod = 'QPSK'
    nLayers = 1
    outlen = 8000
    in_ = np.random.randint(2, size = (N, C))
    if N_filler_bits > 1:
        in_[-N_filler_bits:, :] = np.ones((N_filler_bits, C)) * (-1)
    run_nrRateMatchLDPC(in_, outlen, rv, mod, nLayers, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    test_nrRateMatchLDPC(3960, 1, 1, 20, _eng)
    _eng.quit()