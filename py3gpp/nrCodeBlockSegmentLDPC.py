import numpy as np

from py3gpp.nrDLSCHInfo import getCBSInfo

def nrCodeBlockSegmentLDPC(blk, bgn):
    assert bgn in [1, 2], "bgn must be in [1, 2]"
    cbsInfo = getCBSInfo(len(blk), bgn)
    cbs = None
    return cbs

