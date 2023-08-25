import numpy as np
import scipy as sp
from importlib_resources import files, as_file # importlib.resources only works for Python >= 3.9
from py3gpp.nrDLSCHInfo import getZlist, getZarray
from py3gpp import codes

def nrLDPCDecode(in_, bgn, maxNumIter):
    rxcbs = []
    actualniters = 0
    return rxcbs, actualniters

if __name__ == '__main__':
    bgn = 2
    C = 2
    K = 2560
    F = 36
    cbs = np.ones((K - F, C))
    fillers = (-1) * np.ones((F, C))
    txcbs = np.vstack((cbs, fillers))
    from py3gpp import nrLDPCEncode
    txcodedcbs = nrLDPCEncode(txcbs, bgn)

    # convert to rx soft bits
    rxcodedcbs = (1 - 2 * txcodedcbs.astype(np.double))

    # replace filler bits with 0
    fill_indices = (rxcodedcbs[:, 0] == -1)
    rxcodedcbs[fill_indices, :] = 0

    [rxcbs, actualniters] = nrLDPCDecode(rxcodedcbs, bgn, 25)
