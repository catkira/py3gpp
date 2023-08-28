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
    # but rate = K / N seems correct, because N is the transmitted number of bits
    rate = K / N
 
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
    print(f'block length B = {in_.shape[0]}, number of information bits K = {K}, code rate R = {rate}, i_ls = {i_ls}')

    bm = _load_basegraph(i_ls, bgn)
    # pcm = _lift_basegraph(bm, Zc)

    Slen = np.sum(bm != -1)
    mb, nb = bm.shape
    rxcbs = np.zeros((K, C), np.uint8)

    for c_idx in range(C):
        print(f'decoding segment {c_idx} ...')
        treg = np.zeros((np.max(np.sum(bm != -1, axis = 1)), Zc)) # register storage for minsum
        R = np.zeros((Slen, Zc))
        L = in_[:, c_idx]
        itr = 0
        while itr < maxNumIter:
            Ri = 0
            for lyr in range(mb):
                ti = 0 # number of non -1 in row = lyr
                for col in np.where(bm[lyr, :] != -1)[0]:
                    # subtraction
                    L[col * Zc :][: Zc] -= R[Ri, :]
                    # row alignment and store in treg
                    treg[ti, :] = _mul_sh(L[col * Zc :][: Zc], bm[lyr, col])
                    ti += 1
                    Ri += 1
                # minsum on treg
                if False:
                    for i1 in range(Zc):
                        pos = np.argmin(np.abs(treg[:ti, i1]))
                        min1 = np.abs(treg[pos, i1]) # first minimum
                        temp = np.delete(treg[:, i1], pos)
                        min2 = np.min(np.abs(temp)) # second minimum
                        S = 2 * (treg[:ti, i1] >= 0) - 1
                        parity = np.prod(S)
                        treg[:ti, i1] = min1
                        treg[pos, i1] = min2
                        treg[:ti, i1] *= parity * S # assign signs
                        # print(f'min1 = {min1}, min2 = {min2}, parity = {parity}')
                else:
                    # vectorized version of minsum
                    pos = np.argmin(np.abs(treg[:ti, :]), axis = 0)
                    min1 = np.abs(np.take(treg, pos)) # first minimum
                    temp = np.copy(treg[:ti,:])
                    for i in range(Zc):
                        temp[pos[i]] = np.inf

                    min2 = np.min(np.abs(temp), axis = 0) # second minimum
                    S = 2 * (treg[:ti, :] >= 0) - 1
                    parity = np.prod(S, axis = 0)
                    treg[:ti, :] = np.reshape(np.tile(min1, ti), (ti, Zc))
                    for i in range(Zc):
                        treg[:ti, i] = min2[pos[i]]
                    # treg[pos, :] = min2
                    # np.put_along_axis(treg, pos, min2, axis = 0)
                    treg[:ti, :] *= parity * S # assign signs
                        
                # column alignment, addition and store in R
                Ri -= ti # reset the storage counter
                ti = 0
                for col in np.where(bm[lyr, :] != -1)[0]:
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
    # cbs = np.ones((K - F, C))
    cbs = np.random.randint(2, size = (K - F, C))
    fillers = (-1) * np.ones((F, C))
    txcbs = np.vstack((cbs, fillers))
    from py3gpp import nrLDPCEncode
    txcodedcbs = nrLDPCEncode(txcbs, bgn)

    # replace filler bits with 0
    fill_indices = (txcodedcbs[:, 0] == -1)

    # convert to rx soft bits
    rxcodedcbs = 1 - 2 * txcodedcbs.astype(np.double)

    rxcodedcbs[fill_indices, :] = 0

    import time

    import matlab.engine
    _eng = matlab.engine.connect_matlab()
    st = time.time()
    rxcbs2 = _eng.nrLDPCDecode(rxcodedcbs, bgn, 10)
    et = time.time()
    _eng.quit()
    print(f'decoding with matlab took {et - st} s')

    st = time.time()
    [rxcbs, actualniters] = nrLDPCDecode(rxcodedcbs, bgn, 10)
    et = time.time()
    txcbs[-F:] = 0
    print(f'decoding with python took {et - st} s')
    assert np.array_equal(rxcbs, txcbs)
