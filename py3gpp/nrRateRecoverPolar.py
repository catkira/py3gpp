import numpy as np


def subblock_interleaving(u):
    k = u.shape[-1]
    assert np.mod(k,32)==0, \
        "length for sub-block interleaving must be a multiple of 32."
    y = np.zeros_like(u)    
    # Permutation according to Tab 5.4.1.1-1 in 38.212
    perm = np.array([0, 1, 2, 4, 3, 5, 6, 7, 8, 16, 9, 17, 10, 18, 11, 19,
                        12, 20, 13, 21, 14, 22, 15, 23, 24, 25, 26, 28, 27,
                        29, 30, 31])

    for n in range(k):
        i = int(np.floor(32*n/k))
        j = perm[i] * k/32 + np.mod(n, k/32)
        j = int(j)
        y[n] = u[j]

    return y                        

def nrRateRecoverPolar(llr, K, N, ibil=False):
    if N <= llr.shape[0]:
        # shortening (reverse repetition)
        if ibil == True:
            print("Error: interleaving of coded bits is not implemented!")
            exit()
        rec = llr[subblock_interleaving(np.arange(N))]
    else:
        # TODO
        print("Error!")
        exit()
    return rec