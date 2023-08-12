import numpy as np

from py3gpp.nrDLSCHInfo import getCBSInfo
from py3gpp.nrCRCEncode import nrCRCEncode

def nrCodeBlockSegmentLDPC(blk, bgn):
    assert bgn in [1, 2], "bgn must be in [1, 2]"
    cbsInfo = getCBSInfo(len(blk), bgn)
    assert cbsInfo['Lcb'] in [0, 24], f'Error: Lcb = {cbsInfo["Lcb"]} is not supported!'
    cbs = np.ones((cbsInfo['K'], cbsInfo['C']), dtype=int) * (-1) # fill bits are -1
    idx = 0
    for i in np.arange(cbsInfo['C']):
        if i < cbsInfo['C'] - 1:
            if cbsInfo['Lcb'] == 0:
                cbs[0:cbsInfo['CBZ'], i] = blk[idx:][:cbsInfo['CBZ']]
            elif cbsInfo['Lcb'] == 24:
                cbs[0:cbsInfo['CBZ'] + cbsInfo['Lcb'], i] = nrCRCEncode(blk[idx:][:cbsInfo['CBZ']], '24B', 0)
            idx += cbsInfo['CBZ']
        else:
            if cbsInfo['Lcb'] == 0:
                cbs[0:len(blk) - idx, i] = blk[idx:]
            elif cbsInfo['Lcb'] == 24:
                cbs[0:len(blk) - idx + cbsInfo['Lcb'], i] = nrCRCEncode(blk[idx:], '24B', 0)
            
    return cbs

