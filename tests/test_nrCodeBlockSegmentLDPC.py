import numpy as np
from py3gpp.nrCodeBlockSegmentLDPC import nrCodeBlockSegmentLDPC

if __name__ == '__main__':
    bgn = 2
    blk = np.ones((4001, 1))
    nrCodeBlockSegmentLDPC(blk, bgn)