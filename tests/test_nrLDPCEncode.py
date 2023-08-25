import numpy as np
import pytest
from py3gpp.nrLDPCEncode import nrLDPCEncode

@pytest.mark.parametrize("K", [2560])
@pytest.mark.parametrize("C", [1, 2, 3])
@pytest.mark.parametrize("F", [36])
@pytest.mark.parametrize("bgn", [2])
def test_nrLDPCEncode(K, C, F, bgn):
    cbs = np.random.randint(2, size = (K - F, C))
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    codedcbs_1 = nrLDPCEncode(cbs.copy(), bgn, algo = 'sionna')
    codedcbs_2 = nrLDPCEncode(cbs.copy(), bgn, algo = 'thangaraj')
    assert np.array_equal(codedcbs_1, codedcbs_2)

if __name__ == '__main__':
    bgn = 2
    C = 2
    K = 2560
    F = 36
    test_nrLDPCEncode(K, C, F, bgn)
