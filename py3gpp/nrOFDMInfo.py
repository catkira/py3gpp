import numpy as np

def nrOFDMInfo(carrier = None, nrb = None, scs = None):
    if nrb is None or scs is None:
        if carrier is None:
            print("Error: carrier is needed when no nrb or scs is given!")
            return
        nrb = carrier.NSizeGrid
        scs = carrier.SubcarrierSpacing

    for i in range(20):
        if 2**(i) * 0.85 >= nrb * 12 :
            Nfft = 2**i
            break
    info = dict()
    info['Nfft'] = Nfft
    return info
    