import numpy as np
from py3gpp.nrPBCHDMRSIndices import nrPBCHDMRSIndices


def nrPBCHIndices(ibar):
    indices = np.hstack((np.arange(240, 480), np.arange(480, 528), np.arange(672, 720), np.arange(720, 960)))
    return np.setdiff1d(indices, nrPBCHDMRSIndices(ibar))
