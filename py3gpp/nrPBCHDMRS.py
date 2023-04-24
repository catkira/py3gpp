import numpy as np
from py3gpp.nrPRBS import nrPRBS
from py3gpp.nrSymbolModulate import nrSymbolModulate


def nrPBCHDMRS(ncellid, ibar_SSB):
    assert ncellid >= 0 and ncellid <= 1007
    assert ibar_SSB >= 0 and ibar_SSB <= 7

    c_init = nrPBCHDMRScinit(ibar_SSB, ncellid)
    c = nrPRBS(c_init, 2*144)

    return nrSymbolModulate(c, 'qpsk')

def nrPBCHDMRScinit(issb, ncellid):
    return 2**11 * (issb + 1) * (ncellid//4 + 1) + 2**6 * (issb + 1) + (ncellid % 4)
