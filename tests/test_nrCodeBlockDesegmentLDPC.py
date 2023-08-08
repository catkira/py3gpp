import numpy as np
from py3gpp.nrCodeBlockDesegmentLDPC import nrCodeBlockDesegmentLDPC
from py3gpp.nrCRCDecode import nrCRCDecode

import test_data.ldpc

def test_single_segment():
    bgn = 2
    blklen = 640 + 16 # 16 bit transport block CRC
    rx_blk, err = nrCodeBlockDesegmentLDPC(test_data.ldpc.decBits, bgn, blklen)
    assert np.all(rx_blk == test_data.ldpc.blk)
    assert err == False
    # check transport block CRC
    out, crc = nrCRCDecode(rx_blk, '16')
    assert crc == 0
    assert np.all(out == test_data.ldpc.sib1bits)

if __name__ == '__main__':
    test_single_segment()