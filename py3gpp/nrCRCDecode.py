import numpy as np
from py3gpp.nrCRCEncode import nrCRCEncode

def nrCRCDecode(blkcrc, poly, mask=0):
    encoded = nrCRCEncode(blkcrc, poly, mask)
    L = len(encoded) - len(blkcrc)
    crc = encoded[-L:]
    return encoded[:len(blkcrc) - L], np.any(crc) == False

def test_nrCRCDecode():
    testdata = [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result == True

    testdata = [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result == False