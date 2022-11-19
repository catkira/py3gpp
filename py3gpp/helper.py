import numpy as np

# TS 38.211 Section 5.2.1
def _calc_gold(c_init, length):
    Nc = 1600
    n = 2*length + 1 + 1600
    x1 = np.zeros(n)
    x1[0] = 1
    x2 = np.zeros(n)
    for i in range(30):
        x2[i] = (c_init>>i) & 1

    for i  in np.arange(n-31):
        x1[i + 31] = (x1[i+3] + x1[i])%2
        x2[i + 31] = (x2[i+3] + x2[i+2] + x2[i+1] + x2[i])%2

    c = np.empty(2*length+1, 'bool')
    for n in range(len(c)):
        c[n] = (x1[n+Nc] + x2[n+Nc])%2
    return c