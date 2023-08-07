import numpy as np
from py3gpp.nrCodeBlockSegmentLDPC import nrCodeBlockSegmentLDPC

def array_to_int(data):
    value = 0
    for i in range(len(data)):
        value += (2 ** i) * data[i]
    return value

if __name__ == '__main__':
    bgn = 1
    blk = np.concatenate((np.ones(1000), np.zeros(2000), np.ones(1000))).astype(int)
    cbs1 = nrCodeBlockSegmentLDPC(blk, bgn)
    assert cbs1.shape == (4224, 1)
    assert np.all(cbs1[0:len(blk), 0] == blk)
    # print(f'crc = {array_to_int(cbs1[len(blk):len(blk)+24, 0]):06x}')

    bgn = 2
    blk = np.concatenate((np.ones(1000), np.zeros(2000), np.ones(1000))).astype(int)
    cbs2 = nrCodeBlockSegmentLDPC(blk, bgn)
    assert cbs2.shape == (2080, 2)
    assert np.all(cbs2[0:2000, 0] == blk[0:2000])
    assert np.all(cbs2[0:2000, 1] == blk[2000:])
    for i in range(2):
        print(f'segment {i} crc = {array_to_int(cbs2[2000:2024, i]):06x}')
    assert array_to_int(cbs2[2000:2024, 0]) == 0x271b12
    assert array_to_int(cbs2[2000:2024, 1]) == 0x2875ad
