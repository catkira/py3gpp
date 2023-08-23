import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrRateRecoverPolar import nrRateRecoverPolar

def run_nrRateRecoverPolar(N, eng):
    K = 56
    cw = np.arange(N)
    ref_data = eng.nrRateRecoverPolar(eng.transpose(eng.double(cw)), eng.double(K), eng.double(N))
    ref_data = np.array(list(itertools.chain(*ref_data)))

    data = nrRateRecoverPolar(cw, K, N, False)

    assert (ref_data == data).all()

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("N", [512, 256, 128])
def test_nrRateRecoverPolar(N, eng):
    run_nrRateRecoverPolar(N, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    test_nrRateRecoverPolar(512, _eng)
    _eng.quit()