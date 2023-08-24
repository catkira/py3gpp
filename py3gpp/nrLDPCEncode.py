import numpy as np
from py3gpp.nrDLSCHInfo import getZlist

def nrLDPCEncode(cbs, bgn):
    assert len(cbs.shape) == 2, 'cbs must be a 2-dimensional matrix'
    K = cbs.shape[0]  # length of a code segment
    C = cbs.shape[1]  # number of code segments
    
    # calculate Zc
    if bgn == 1:
        nsys = 22
        ncwnodes = 66
    else:
        nsys = 10
        ncwnodes = 50
    Zc = int(K / nsys)
    assert Zc in getZlist(), f'Zc = {Zc} is not a valid value'

    # calculate output size (N)
    N = int(Zc * ncwnodes)
    codedcbs = np.zeros((N + 2 * Zc, C))

    # replace filler bits with 0
    fill_indices = (cbs[:, 0] == -1)  # filler bits are at identical locations in every segment
    cbs[fill_indices, :] = 0

    # encode

    # set filler bits back to -1
    fill_indices_out = np.append(fill_indices, np.repeat(False, N + 2 * Zc - K))
    codedcbs[fill_indices_out, :] = -1

    # puncture first 2 * Zc systematic bits
    codedcbs = codedcbs[2 * Zc :, :]

    return codedcbs

if __name__ == '__main__':
    bgn = 2
    C = 2
    K = 2560
    F = 36
    cbs = np.ones((K - F, C))
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    codedcbs = nrLDPCEncode(cbs, bgn)
    print(codedcbs.shape)
