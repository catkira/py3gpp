import numpy as np
from py3gpp.nrCodeBlockSegmentLDPC import nrCodeBlockSegmentLDPC
from py3gpp.nrCodeBlockDesegmentLDPC import nrCodeBlockDesegmentLDPC

import test_data.ldpc

def array_to_int(data):
    value = 0
    for i in range(len(data)):
        value += (2 ** i) * data[i]
    return value

def test_single_segment():
    bgn = 2
    blk = nrCodeBlockSegmentLDPC(test_data.ldpc.decBits, bgn)
    # test_data.ldpc.blk contains fill bytes which need to be skipped in the comparison
    assert np.array_equal(blk[:len(test_data.ldpc.blk), 0], test_data.ldpc.blk)
    
def test_single_segment_2():
    bgn = 1
    blk = np.concatenate((np.ones(1000), np.zeros(2000), np.ones(1000))).astype(int)
    cbs1 = nrCodeBlockSegmentLDPC(blk, bgn)
    assert cbs1.shape == (4224, 1)
    assert np.array_equal(cbs1[0:len(blk), 0], blk) 

def test_multi_segment():
    bgn = 2
    blk = np.concatenate((np.ones(1000), np.zeros(2000), np.ones(1000))).astype(int)
    cbs2 = nrCodeBlockSegmentLDPC(blk, bgn)
    assert cbs2.shape == (2080, 2)
    assert np.all(cbs2[0:2000, 0] == blk[0:2000])
    assert np.all(cbs2[0:2000, 1] == blk[2000:])
    for i in range(2):
        print(f'segment {i} crc = {array_to_int(cbs2[2000:2024, i]):06x}')
    assert array_to_int(cbs2[2000:2024, 0]) == 0x271b12
    assert array_to_int(cbs2[2000:2024, 1]) == 0x001724

def test_multi_segment_combined():
    blklen = 10000
    bgn = 1
    data = np.ones(blklen)

    cbs = nrCodeBlockSegmentLDPC(data, bgn)
    data2, err = nrCodeBlockDesegmentLDPC(cbs, bgn, blklen)
    assert err is False
    assert np.array_equal(data, data2)

if __name__ == '__main__':

    test_multi_segment_combined()
    test_multi_segment()

    test_single_segment()
    test_single_segment_2()
    
