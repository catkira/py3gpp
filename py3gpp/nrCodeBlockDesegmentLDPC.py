import numpy as np

from py3gpp.nrDLSCHInfo import getCBSInfo
from py3gpp.nrCRCDecode import nrCRCDecode
from py3gpp.nrDLSCHInfo import getCBSInfo

def nrCodeBlockDesegmentLDPC(cbs, bgn, blklen):
    blk = None
    err = False
    if len(cbs.shape) == 1:
        blk = cbs[:blklen]
        # there is no appended CRC when there is only one segment
    else:
        cbsInfo = getCBSInfo(blklen, bgn)
        idx = 0
        blk = np.zeros(blklen)
        for i in np.arange(cbsInfo['C']):
            if i < cbsInfo['C'] - 1:
                blk[idx:][:cbsInfo['CBZ']] = cbs[0 : cbsInfo['CBZ'], i]
                _, crc = nrCRCDecode(cbs[0 : cbsInfo['CBZ'] + cbsInfo['Lcb'], i], '24B')
                idx += cbsInfo['CBZ']
            else:
                blk[idx:][:blklen - idx] = cbs[0 : blklen - idx, i]
                _, crc = nrCRCDecode(cbs[0 : cbsInfo['CBZ'] + cbsInfo['Lcb'], i], '24B')

            if crc != 0:
                err = True
                print(f'nrCodeBlockDesegmentLDPC: crc error in segment {i}')

    return blk, err
