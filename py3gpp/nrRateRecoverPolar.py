import numpy as np

def subblock_interleaving(u):
    N = u.shape[-1]
    assert np.mod(N,32)==0, \
        "length for sub-block interleaving must be a multiple of 32."
    y = np.zeros_like(u)    
    # Permutation according to Tab 5.4.1.1-1 in 38.212
    perm = np.array([0, 1, 2, 4, 3, 5, 6, 7, 8, 16, 9, 17, 10, 18, 11, 19,
                     12, 20, 13, 21, 14, 22, 15, 23, 24, 25, 26, 28, 27,
                     29, 30, 31])

    for n in range(N):
        i = int(32*n/N)
        j = int(perm[i] * N/32 + np.mod(n, N/32))
        y[n] = u[j]

    return y                        

# nrRateRecoverPolar() in Matlab discards all repeated llr values,
# this is not optimal but we make this function behave the same by default
# optimal behaviour can be switched on by setting discardRepetition to False
def nrRateRecoverPolar(llr, K, N, ibil=False, discardRepetition=True):
    E = llr.shape[0]
    if N <= E:
        # undo repetition
        y = np.copy(llr[:N])
        if discardRepetition == False:
            for k in range(N, E):
                y[k%N] += llr[k]
    else:
        # TODO: implement shortening und puncturing
        print("Error!")
        exit()
    if ibil == True:
        print("Error: interleaving of coded bits is not implemented!")
        exit()
    d = np.zeros(N)
    np.put(d, subblock_interleaving(np.arange(N)), y)
    return d
