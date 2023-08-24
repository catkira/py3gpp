import numpy as np
from py3gpp.nrRateRecoverLDPC import nrRateRecoverLDPC
import test_data.ldpc

def test_nrRateRecoverLDPC():
    # test data from SIB1 decoding with Matlab
    rv = 0
    mod = 'QPSK'
    nLayers = 1
    trblklen = 640
    R = 0.3701
    raterec = nrRateRecoverLDPC(test_data.ldpc.cw, trblklen, R, rv, mod, nLayers)
    assert np.array_equal(raterec[:, 0], test_data.ldpc.raterec)

if __name__ == '__main__':
    test_nrRateRecoverLDPC()