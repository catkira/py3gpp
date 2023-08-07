import numpy as np
from py3gpp.nrCodeBlockDesegmentLDPC import nrCodeBlockDesegmentLDPC
from py3gpp.nrCRCDecode import nrCRCDecode

from test_data.ldpc import *

def test_single_segment():
    bgn = 2
    blklen = 656
    rx_blk, err = nrCodeBlockDesegmentLDPC(decBits, bgn, blklen)
    assert np.all(rx_blk == blk)
    assert err == False
    # check transport block CRC
    out, crc = nrCRCDecode(rx_blk, '16')
    assert crc == 0
    assert np.all(out == sib1bits)

if __name__ == '__main__':
    test_single_segment()