import numpy as np
from py3gpp.nrPolarEncode import nrPolarEncode
from py3gpp.nrRateMatchPolar import nrRateMatchPolar
from py3gpp.nrCRCEncode import nrCRCEncode
from py3gpp.nrPBCHPRBS import nrPBCHPRBS


def nrBCH(trblk, sfn, hrf, lssb, idxoffset, ncellid):
    return np.zeros(864, int)

if __name__ == '__main__':
    trblk = np.zeros(24, int)
    sfn = 0
    hrf = 0
    lssb = 8
    idxoffset = 0
    ncellid = 0
    nrBCH(trblk, sfn, hrf, lssb, idxoffset, ncellid)