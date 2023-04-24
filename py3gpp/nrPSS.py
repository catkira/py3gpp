import numpy as np
from py3gpp.helper import _calc_m_seq

def nrPSS(ncellid):
    assert ncellid >= 0 and ncellid <= 1007, "invalid ncellid"
    N = 7
    c = [0, 1, 1, 0, 1, 1, 1]
    taps = [0, 4]
    m = _calc_m_seq(N, c, taps)
    d_PSS = 1 - 2 * np.roll(m, -nrPSSv(ncellid))
    return d_PSS

def nrPSSv(ncellid):
    n2 = ncellid % 3
    return 43*n2
