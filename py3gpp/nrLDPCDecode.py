import numpy as np
import scipy as sp
from importlib_resources import files, as_file # importlib.resources only works for Python >= 3.9
from py3gpp.nrDLSCHInfo import getZlist, getZarray
from py3gpp import codes
from py3gpp.nrLDPCEncode import _load_basegraph, _lift_basegraph, _mul_sh

def nrLDPCDecode(in_, bgn, maxNumIter):
    assert len(in_.shape) == 2, 'cbs must be a 2-dimensional matrix'
    C = in_.shape[1]  # number of code block segments

    if bgn == 1:
        ncwnodes = 66
    else:
        ncwnodes = 50

    N = in_.shape[0]  # length of a code word
    assert 0 < N < (316 * 384) + 1, 'N = {N} is an unsupported code length'

    Zc = int(N / ncwnodes)
    assert Zc in getZlist(), f'Zc = {Zc} is not supported'
    assert Zc == N / ncwnodes, f'N = {N} and ncwnodes = {ncwnodes} is not a valid combination'

    # add punctured 2 * Zc bits
    in_ = np.concatenate((np.zeros((2 * Zc, C)), in_))
    B = in_.shape[0]
    
    if bgn == 1:
        k_b = 22
    else:
        if B > 640: # TODO: is it ok to use B instead of N here?
            k_b = 10
        elif B > 560:
            k_b = 9
        elif B > 192:
            k_b = 8
        else:
            k_b = 6
    K = Zc * k_b
    # calulating R = K / B is another possibility and gives a slightly different number,
    # but R = K / N seems correct, because N is the transmitted number of bits
    R = K / N
 
    Zarray = getZarray()
    min_val = 100000
    i_ls = None
    for i, s in enumerate(Zarray):
        for s1 in s:
            x = k_b * s1
            if  x >= K:
                # valid solution
                if x < min_val:
                    min_val = x
                    i_ls = i
    assert i is not None, 'could not find i_ls'
    print(f'block length B = {in_.shape[0]}, number of information bits K = {K}, code rate R = {R}, i_ls = {i_ls}')

    bm = _load_basegraph(i_ls, bgn)
    pcm = _lift_basegraph(bm, Zc)
    num_cns = pcm.shape[0] # total number of check nodes
    num_vns = pcm.shape[1] # total number of variable nodes

    Slen = np.sum(bm != -1)
    R = np.zeros((Slen, Zc))
    treg = np.zeros((np.max(np.sum(bm != -1, axis = 1)), Zc)) # register storage for minsum
    mb, nb = bm.shape
    rxcbs = np.zeros((K, C), np.uint8)

    for c_idx in range(C):
        print(f'decoding segment {i} ...')
        L = in_[:, c_idx]
        itr = 0
        while itr < maxNumIter:
            Ri = 0
            for lyr in range(mb):
                ti = 0
                for col in range(nb):
                    if bm[lyr, col] != -1:
                        # subtraction
                        L[col * Zc :][: Zc] -= R[Ri, :]
                        # row alignment and store in treg
                        treg[ti, :] = _mul_sh(L[col * Zc :][: Zc], bm[lyr, col])
                        ti += 1
                        Ri += 1
            # minsum on treg
            for i1 in range(Zc):
                pos = np.argmin(np.abs(treg[:ti, i1]))
                min1 = np.abs(treg[pos, i1]) # first minimum
                temp = np.concatenate((treg[: pos - 1], treg[pos + 1 :]))
                min2 = np.min(np.abs(temp)) # second minimum
                S = 2 * (treg[:ti, i1] >= 0) - 1
                parity = np.prod(S)
                treg[:, i1] = min1
                treg[pos, i1] = min2
                treg[:ti, i1] *= parity * S * treg[:ti, i1] # assign signs
                # for j in range(ti):
                    
            # column alignment, addition and store in R
            Ri = Ri - ti # reset the storage counter
            ti = 0
            for col in range(nb):
                if bm[lyr, col] != -1:
                    # column alignment 
                    R[Ri, :] = _mul_sh(treg[ti, :], Zc - bm[lyr, col])
                    # addition
                    L[col * Zc :][: Zc] += R[Ri, :]
                    Ri += 1
                    ti += 1

            rxcbs[:, c_idx] = np.array(L[:K] < 0).astype(np.uint8)
            itr += 1

    actualniters = itr
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
    txcbs[-F:] = 0
    assert np.array_equal(rxcbs, txcbs)
