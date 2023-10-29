
import numpy as np
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.nrPRBS import nrPRBS

def nrPDSCH(cws, modulation, nlayers, nid, nrnti):
    if nlayers != 1:
        raise NotImplementedError('not ready yet')
    assert nlayers in list(range(1, 9))

    if nlayers > 4:
        ncw = 2
    else:
        ncw = 1

    scrambled_bits = []
    res_sym = []
    for i in range(ncw):
        databits = cws[i]
        cinit = (nrnti * 2**15) + (i * 2**14) + nid
        prbs_bits = nrPRBS(cinit, len(databits))
        scrambled_bits.append(np.bitwise_xor(databits, prbs_bits))
        scrambled_bits = np.array(scrambled_bits)

        res_sym.append(nrSymbolModulate(scrambled_bits[i], modulation[i]))

    # TODO
    # res_sym = nrLayerMap(res_sym, nlayers)
    # res_sym = np.hstack(res_sym)

    return np.array(res_sym)
