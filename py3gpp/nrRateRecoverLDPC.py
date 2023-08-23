import numpy as np
from py3gpp.nrDLSCHInfo import getZlist
from py3gpp.nrDLSCHInfo import nrDLSCHInfo

def nrRateRecoverLDPC(in_, trblklen, R, rv, mod, nLayers, numCB = None):
    assert (R > 0) and (R < 1), 'R has to be 0 < R < 1'
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

    cbsinfo = nrDLSCHInfo(trblklen, R)
    bgn = cbsinfo['BGN']
    Zc = cbsinfo['Zc']
    N = cbsinfo['N']

    C = cbsinfo['c'] if numCB is None else numCB
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
    k0 = int(k0)

    G = len(in_)
    out = np.zeros((N, C))
    idx = 0
    for r in np.arange(C):
        if r <= C - np.mod(G / (nLayers * Qm), C) - 1:
            E = Qm * nLayers * np.floor(G / (Qm * nLayers * C)).astype(int)
        else:
            E = Qm * nLayers * np.ceil(G / (Qm * nLayers * C)).astype(int)
        
        # pad unknown bits
        if G < E:
            deconcatenated = np.append(in_, np.zeros(E-G))
        else:
            deconcatenated = in_[idx : idx + E]
        idx += E

        out[:, r] = _rateRecover(deconcatenated, cbsinfo, k0, Ncb, Qm)
    return out

def _rateRecover(in_, cbsinfo, k0, Ncb, Qm):
    # perform deinterleaving according to section 5.4.2.2
    E = len(in_)
    in_ = np.reshape(in_, (int(E / Qm), Qm)).ravel('F')

    # puncture systematic bits and remove fill bits
    K = int(cbsinfo['K'] - 2 * cbsinfo['Zc'])
    Kd = int(K - cbsinfo['F'])

    N_filler_bits = int(np.min((K, Ncb)) - Kd)

    N_buffer = Ncb - N_filler_bits
    idx = np.tile(np.arange(Ncb), np.ceil(E / N_buffer).astype(int))

    idx = np.roll(idx, -k0)

    indices = np.delete(idx, (idx >= Kd) & (idx < K))
    indices = indices[:E]

    out = np.zeros(cbsinfo['N'])
    out[Kd : K] = np.inf

    if E > N_buffer:
        for i in np.arange(np.floor(E / N_buffer).astype(int)):
            out[indices[:N_buffer]] += in_[i * N_buffer : (i + 1) * N_buffer]

        rem_bits = np.mod(E, N_buffer)
        out[indices[:rem_bits]] +=  in_[-rem_bits:]

    else:
        out[indices] = in_

    return out

if __name__ == '__main__':
    sbits = np.ones(4500)
    trblklen = 4000
    R = 0.5
    rv = 1
    mod = 'QPSK'
    nLayers = 1
    numCB = 1
    raterec = nrRateRecoverLDPC(sbits, trblklen, R, rv, mod, nLayers, numCB)
    print(raterec.shape)