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

@pytest.mark.parametrize("N", [512, 256, 128])
def test_nrRateMatchLDPC(N, eng):
    rv = 0
    mod = 'QPSK'
    nLayers = 1
    outlen = 8000
    in_ = np.ones((3960,2))
    run_nrRateMatchLDPC(in_, outlen, rv, mod, nLayers, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    test_nrRateMatchLDPC(512, _eng)
    _eng.quit()