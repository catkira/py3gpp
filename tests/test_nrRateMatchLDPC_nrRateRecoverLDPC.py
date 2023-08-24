import numpy as np
from py3gpp.nrRateRecoverLDPC import nrRateRecoverLDPC
from py3gpp.nrRateMatchLDPC import nrRateMatchLDPC

def test_nrRateMatchLDPC_nrRateRecoverLDPC():
    rv = 0
    mod = 'QPSK'
    nLayers = 1
    outlen = 8000
    in_ = np.ones((3960, 2))
    rematched = nrRateMatchLDPC(in_, outlen, rv, mod, nLayers)
    
    trblklen = 0
    R = 0.5
    out = nrRateRecoverLDPC(rematched, trblklen, R, rv, mod, nLayers)
    pass # TODO: add a useful test here

if __name__ == '__main__':
    test_nrRateMatchLDPC_nrRateRecoverLDPC()