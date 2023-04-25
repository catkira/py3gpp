
# 38.211 7.4.3 SS/PBCH block

import numpy as np
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.nrPBCHPRBS import nrPBCHPRBS

def nrPBCH(ncellid, v, databits):
    n = len(databits)

    assert ncellid <= 1007 and ncellid >= 0
    assert v >= 0 and v <= 7
    assert n > 0

    # Scrambling, Section 7.3.3.1, TS 38.211
    prbs_bits = nrPBCHPRBS(ncellid, v, n)
    scrambled_bits = np.bitwise_xor(databits, prbs_bits)

    # Modulation, Section 7.3.3.2, TS 38.211
    res_sym = nrSymbolModulate(scrambled_bits, 'QPSK')

    return np.array(res_sym)
