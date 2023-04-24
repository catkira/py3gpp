import numpy as np
from py3gpp.helper import _calc_m_seq

def _gold(N_id_1, N_id_2):
    N = 7
    c = [1, 0, 0, 0, 0, 0, 0]
    taps_0 = [0, 4]
    taps_1 = [0, 1]
    mseq_0 = _calc_m_seq(N, c, taps_0)
    mseq_1 = _calc_m_seq(N, c, taps_1)
    m_0 = 15 * int((N_id_1 / 112)) + 5 * N_id_2
    m_1 = N_id_1 % 112
    d_SSS = (1 - 2 * np.roll(mseq_0, -m_0)) * (1 - 2 * np.roll(mseq_1, -m_1))
    return d_SSS


def nrSSS(ncellid):
    assert ncellid >= 0 and ncellid <= 1007, "invalid ncellid"
    N_id_2 = ncellid % 3
    N_id_1 = (ncellid - N_id_2) // 3
    return _gold(N_id_1, N_id_2)
