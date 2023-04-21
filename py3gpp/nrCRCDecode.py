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
