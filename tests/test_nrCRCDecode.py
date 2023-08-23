import numpy as np
from py3gpp.nrCRCDecode import nrCRCDecode

def test_nrCRCDecode():
    testdata = np.array([0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0])
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result == 0
    assert np.array_equal(data[:, 0], testdata[0 : len(testdata) - 24])

    testdata = np.array([1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0])
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result != 0
    assert np.array_equal(data[:, 0], testdata[0 : len(testdata) - 24])

if __name__ == '__main__':
    test_nrCRCDecode()