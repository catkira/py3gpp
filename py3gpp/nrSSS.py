import numpy as np


def _calc_m_seq_0():
    n = 127
    x = np.zeros(n, "int32")  # m-sequence
    x[0:7] = np.array([1, 0, 0, 0, 0, 0, 0])
    for i in np.arange(0, n - 7):
        x[i + 7] = (x[i + 4] + x[i]) % 2
    return x


def _calc_m_seq_1():
    n = 127
    x = np.zeros(n, "int32")  # m-sequence
    x[0:7] = np.array([1, 0, 0, 0, 0, 0, 0])
    for i in np.arange(0, n - 7):
        x[i + 7] = (x[i + 1] + x[i]) % 2
    return x


def _gold(N_id_1, N_id_2):
    n = 127
    x_0 = _calc_m_seq_0()
    x_1 = _calc_m_seq_1()
    d_SSS = np.zeros(n, "int32")
    m_0 = 15 * int((N_id_1 / 112)) + 5 * N_id_2
    m_1 = N_id_1 % 112
    for n in np.arange(0, 127):
        d_SSS[n] = (1 - 2 * x_0[(n + m_0) % 127]) * (1 - 2 * x_1[(n + m_1) % 127])
    return d_SSS


def nrSSS(ncellid):
    N_id_2 = ncellid % 3
    N_id_1 = (ncellid - N_id_2) // 3
    return _gold(N_id_1, N_id_2)
