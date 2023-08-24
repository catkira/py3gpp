import numpy as np

def nrLDPCEncode(cbs, bgn):
    codedcbs = np.empty(0)
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
