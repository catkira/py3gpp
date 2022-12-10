import numpy as np

def nrRateRecoverPolar(llr, K, N, ibil=False):
    if N <= llr.shape[0]:
        rec = llr[:llr.shape[0]]
    else:
        # TODO
        print("Error!")
        exit()
    return rec