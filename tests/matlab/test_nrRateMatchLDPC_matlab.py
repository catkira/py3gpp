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

@pytest.mark.parametrize("N", [3960, 8000])  # BGN1 & BGN2
@pytest.mark.parametrize("C", [1, 2, 3])
@pytest.mark.parametrize("rv", [0, 1, 2, 3])
@pytest.mark.parametrize("mod", ["QPSK", "64QAM", "256QAM"])
@pytest.mark.parametrize("nLayers", [1, 2, 3, 4])
@pytest.mark.parametrize("N_filler_bits", [0, 20])
def test_nrRateMatchLDPC_matlab(N, C, rv, mod, nLayers, N_filler_bits, eng):
    outlen = 8000
    in_ = np.random.randint(2, size = (N, C))
    if N_filler_bits > 1:
        in_[-N_filler_bits:, :] = np.ones((N_filler_bits, C)) * (-1)
    run_nrRateMatchLDPC(in_, outlen, rv, mod, nLayers, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    N = 3960
    C = 1
    rv = 0
    mod = 'QPSK'
    nLayers = 1
    N_filler_bits = 20
    test_nrRateMatchLDPC_matlab(N, C, rv, mod, nLayers, N_filler_bits, _eng)
    _eng.quit()