import numpy as np
from py3gpp.nrDLSCHInfo import getZlist

def nrRateMatchLDPC(in_, outlen, rv, mod, nLayers):
    assert nLayers == 1, 'nLayers > 1 is not yet implemented'
    assert rv in [0, 1, 2, 3], 'rv has to be in [0, 1, 2, 3]'
    if mod in ['pi/2-BPSK', 'BPSK']:
        Qm = 1
    elif mod == 'QPSK':
        Qm = 2
    elif mod == '16QAM':
        Qm = 4
    elif mod == '64QAM':
        Qm = 6
    elif mod == '256QAM':
        Qm = 8
    else:
        assert False, f'modulation type {mod} is not supported'
    N = in_.shape[0] # length of each code word
    C = in_.shape[1] # number of code words within this transport block
    Zlist = np.array(getZlist())
    if N in Zlist * 66:
        bgn = 1
        ncwnodes = 66
    elif N in Zlist * 50:
        bgn = 2
        ncwnodes = 50
    else:
        assert False, f'N = {N} is not supported'
    Zc = int(N / ncwnodes)

    Ncb = N

    if bgn == 1:
        if rv == 0:
            k0 = 0
        elif rv == 1:
            k0 = np.floor(17 * Ncb / N) * Zc
        elif rv == 2:
            k0 = np.floor(33 * Ncb / N) * Zc
        elif rv == 3:
            k0 = np.floor(56 * Ncb / N) * Zc
    elif bgn == 2:
        if rv == 0:
            k0 = 0
        elif rv == 1:
            k0 = np.floor(13 * Ncb / N) * Zc
        elif rv == 2:
            k0 = np.floor(25 * Ncb / N) * Zc
        elif rv == 3:
            k0 = np.floor(43 * Ncb / N) * Zc
    rematched = np.empty(0)
    for r in np.arange(C):
        if r <= C - np.mod(outlen / (nLayers * Qm), C) - 1:
            E = Qm * nLayers * np.floor(outlen / (Qm * nLayers * C)).astype(int)
        else:
            E = Qm * nLayers * np.ceil(outlen / (Qm * nLayers * C)).astype(int)
        rematched = np.append(rematched, _rateMatch(in_[:, r], E, k0, Ncb, Qm))

    return rematched

def _rateMatch(d, E, k0, Ncb, Qm):
    N_filler_bits = np.count_nonzero(d[:Ncb] == -1)

    if np.ceil(E / (len(d[:Ncb]) - N_filler_bits)):
        d = np.append(d, d)

    d = np.roll(d, -k0)

    e = d[d != -1][:E]
    return e

if __name__ == '__main__':
    rv = 0
    mod = 'QPSK'
    nLayers = 1
    outlen = 8000
    in_ = np.ones((3960,2))
    rematched = nrRateMatchLDPC(in_, outlen, rv, mod, nLayers)
    assert rematched.shape == (8000,)