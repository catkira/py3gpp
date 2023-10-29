import numpy as np
from py3gpp.nrSymbolDemodulate import nrSymbolDemodulate
from py3gpp.nrPRBS import nrPRBS

def nrPDSCHDecode(sym, mod, nid, rnti):
    descrambled_bits = []
    n_layers = sym.shape[0]
    if n_layers != 1:
        raise NotImplementedError('not ready yet')

    for i in range (n_layers):
        demod_sym = nrSymbolDemodulate(sym[i], mod[i])
        cinit = (rnti * 2**15) + (i * 2**14) + nid
        prbs_bits = nrPRBS(cinit, len(demod_sym))
        descrambled_bits.append(np.multiply(demod_sym, (-prbs_bits*2 + 1)))
        descrambled_bits = np.array(descrambled_bits)
    return descrambled_bits



if __name__ == '__main__':
    modulation = ['16QAM']
    nlayers = 1
    ncellid = 42
    rnti = 6143
    data = np.random.randint(0, 2, size=(1, 8000))
    import py3gpp
    txsym = py3gpp.nrPDSCH(data, modulation, nlayers, ncellid, rnti)
    rxbits = nrPDSCHDecode(txsym, modulation, ncellid, rnti)
    assert np.array_equal(data, np.round(rxbits<0).astype(int))
