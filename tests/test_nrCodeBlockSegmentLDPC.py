import numpy as np
from py3gpp.nrCodeBlockSegmentLDPC import nrCodeBlockSegmentLDPC

if __name__ == '__main__':
    bgn = 1
    blk = np.arange(4000)
    cbs1 = nrCodeBlockSegmentLDPC(blk, bgn)
    assert cbs1.shape == (4224, 1)
    assert np.all(cbs1[0:len(blk), 0] == blk)
    print(f'crc = {cbs1[len(blk), 0]:02x} {cbs1[len(blk+1), 0]:02x} {cbs1[len(blk+2), 0]:02x}')

    bgn = 2
    blk = np.arange(4000)
    cbs2 = nrCodeBlockSegmentLDPC(blk, bgn)
    assert cbs2.shape == (2080, 2)
    assert np.all(cbs2[0:2000, 0] == blk[0:2000])
    assert np.all(cbs2[0:2000, 1] == blk[2000:])
    for i in range(2):
        print(f'segment {i} crc = {cbs2[2000, i]:02x} {cbs2[2001, i]:02x} {cbs2[2002, i]:02x}')
