import numpy as np
from .helper import _calc_gold

def nrPBCHDMRS(ncellid, ibar_SSB):
    # ibar_SSB is a 3 bit value
    c_init = 2**11 * (ibar_SSB+1)*(ncellid//4+1) + 2**6 * (ibar_SSB+1) + (ncellid%4)
    c = _calc_gold(c_init, 144)

    r = np.empty(144, 'complex')
    for m in range(len(r)):
        r[m] = 1/np.sqrt(2)*(1-2*c[2*m]) + 1j*1/np.sqrt(2)*(1-2*c[2*m+1])
    return r