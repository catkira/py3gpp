
# 38.211

import numpy as np

from py3gpp.nrPRBS import nrPRBS
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig
from py3gpp.nrPDSCHDMRS import PDSCHDMRSSyms

def nrPDSCHPTRS(cfg: nrPDSCHConfig, carrier: nrCarrierConfig):
    raise NotImplementedError("no ready yet")
    if cfg.EnablePTRS == 0:
        return []

    if cfg.DMRS.DMRSConfigurationType == 1:
        n_dmrs_per_re = 6
    else:
        n_dmrs_per_re = 4
    n_dmrs_bits_re = 2*n_dmrs_per_re

    dmrs_begin = n_dmrs_bits_re * min(cfg.PRBSet)
    dmrs_end = n_dmrs_bits_re * (max(cfg.PRBSet)+1)
    dmrs_size = n_dmrs_bits_re * cfg.NSizeBWP

    n_scid = 0

    occupied_syms = PDSCHDMRSSyms(cfg)

    # Start generation for every symbol
    n_symb = occupied_syms[0]
    cinit_dmrs = PDSCHPTRScinit(carrier.SymbolsPerSlot, carrier.NSlot, n_symb, cfg.DMRS.NIDNSCID, n_scid)
    dmrs_prbs = nrPRBS(cinit_dmrs, dmrs_size)

    # Cut DMRS PRBS sequency
    dmrs_prbs = dmrs_prbs[dmrs_begin:dmrs_end]
    dmrs_syms = nrSymbolModulate(dmrs_prbs, "QPSK")

    # Form PTRS symbols from DMRS l0 sequency
    # TODO

    return []

# LUT for PTRS occupied symbols positions
def PDSCHPTRSSyms(carrier: nrCarrierConfig, cfg: nrPDSCHConfig):
    # First get DMRS symbols
    dmrs_syms = PDSCHDMRSSyms(cfg)
    # Then calculate positions of PTRS
    A_pos = cfg.DMRS.DMRSTypeAPosition
    td = cfg.PTRS.TimeDensity

    ptrs_cnt = td-1
    occupied_syms = np.array([], dtype=int)
    for i in range(cfg.SymbolAllocation[0], carrier.SymbolsPerSlot):
        if i == A_pos:
            # print(i, 'flag A position')
            ptrs_cnt = 0
            continue

        if i in dmrs_syms:
            # print(i, 'flag DMRS')
            ptrs_cnt = 0
            continue

        ptrs_cnt += 1

        if ptrs_cnt == td:
            # print(i, ptrs_cnt, 'mark')
            occupied_syms = np.append(occupied_syms, i)
            ptrs_cnt = 0

    return occupied_syms

def PDSCHPTRScinit(sps, n_slot, n_symb, NIDSCID, n_scid):
    return 2**17 * (sps * n_slot + n_symb + 1) * (2*NIDSCID + 1) + 2*NIDSCID + n_scid