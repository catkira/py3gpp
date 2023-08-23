import numpy as np
from py3gpp.nrCRCDecode import nrCRCDecode

def test_nrCRCDecode():
    testdata = np.array([0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0])
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result == 0

    testdata = np.array([1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0])
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result != 0

if __name__ == '__main__':
    test_nrCRCDecode()