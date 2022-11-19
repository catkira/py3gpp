import numpy as np

def nrPSS(N_id_2):
    n = 127
    x = np.zeros(n, 'int32')    # m-sequence
    x[0:7] = np.array([0, 1, 1, 0, 1, 1, 1])
    for i in np.arange(0, 127 - 7):
        x[i+7] = (x[i + 4] + x[i]) % 2
    d_PSS = np.zeros(n, 'int32')
    for n in np.arange(0, 127):
        m = (n + 43*N_id_2) % 127  # offset based on N_id_2
        d_PSS[n] = 1 - 2*x[m]  # BPSK modulation
    return d_PSS