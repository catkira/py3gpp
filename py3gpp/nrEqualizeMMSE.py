import numpy as np

def nrEqualizeMMSE(rxSym, hest, nVar):
    csi = (np.abs(hest * np.conj(hest)) + nVar)
    # rxEq = rxSym / hest # zero forcing
    rxEq = rxSym * np.conj(hest) / csi
    return rxEq, csi