import numpy as np

from py3gpp.nrDLSCHInfo import getCBSInfo
from py3gpp.nrCRCDecode import nrCRCDecode

def nrCodeBlockDesegmentLDPC(cbs, bgn, blklen):
    blk = None
    err = False
    if len(cbs.shape) == 1:
        blk = cbs[:blklen]
        # there is no appended CRC when there is only one segment
    else:
        print('Error: multiple segments are not yet implemented!')
        err = True
    return blk, err