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

def nrRateMatchPolar(enc, K, E, ibil=False):
    # TODO: for what is the parameter K??
    N = enc.shape[0]
    d = np.zeros(N, int)
    d = enc[subblock_interleaving(np.arange(N))]
    y = np.zeros(E, int)
    if N <= E:
        # repetition
        y[:N] = d[:N]
        for k in range(N, E):
            y[k] += d[k%N]
    else:
        # TODO: implement shortening und puncturing
        print("Error!")
        exit()
    if ibil == True:
        print("Error: interleaving of coded bits is not implemented!")
        exit()
    return y

if __name__ == '__main__':
    import py3gpp
    # input = np.zeros(512, int)
    # input[0:3] = [1 , 1, 1]
    input = np.array([1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,1,0,1,0,0,1,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,0,1,1,1,0,1,0,0,1,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,1,0,1,1,1,0,0,1,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,1,0,1,1,0]).astype(int)
    # out_desired = np.array([1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]).astype(int)
    out_desired = np.array([1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,0,0,0,1,0,0,0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,0,1,1,1,0,1,0,0,1,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,1,0,1,1,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,0,0,0,1,0,0,0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0]).astype(int)
    out = nrRateMatchPolar(input, 0, 863, False)
    assert np.array_equal(out, out_desired)