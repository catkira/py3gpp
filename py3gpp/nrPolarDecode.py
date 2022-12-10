import numpy as np

# rec: Rate-recovered input, LLRs, length must be power of two
# K: length of information block in bits, includes CRC
# E: rate-matched output length in bits
# L: length of decoding list
# CRClen: number of appended CRC bits
def nrPolarDecode(rec, K, E, L, padCRC=False, nmax=9, iil=True, CRClen=24):
    decbits = np.empty(K, 'bool')
    if CRClen != 24 and CRClen != 11 and CRClen != 6:
        print("Error: invalid CRClen value!")
        exit()
    if nmax != 9 and nmax != 10:
        print("Error: invalid nmax value!")
        exit()
    return decbits