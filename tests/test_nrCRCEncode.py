import numpy as np
from py3gpp.nrCRCEncode import nrCRCEncode

def test_nrCRCEncode():
    test = np.zeros(32)
    test[0] = 1
    result = nrCRCEncode(test, "24C")
    # fmt: off
    assert np.all(result[:, 0] == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
    # fmt: on

if __name__ == '__main__':
    test_nrCRCEncode()