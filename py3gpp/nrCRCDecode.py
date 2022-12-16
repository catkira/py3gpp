import numpy as np
from py3gpp.nrCRCEncode import nrCRCEncode

def _binToInt(bin):
    integer = 0
    for bit in np.flip(bin):
        integer += bit
        integer <<= 1
    return integer

def nrCRCDecode(blkcrc, poly, mask=0):
    encoded = nrCRCEncode(blkcrc, poly, mask)
    L = len(encoded) - len(blkcrc)
    crc = encoded[-L:]
    return encoded[:len(blkcrc) - L], _binToInt(crc)

def test_nrCRCDecode():
    testdata = [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result == 0

    testdata = [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    data, crc_result = nrCRCDecode(testdata, '24C')
    assert crc_result != 0