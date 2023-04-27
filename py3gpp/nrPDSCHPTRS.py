
# 38.211

import numpy as np

from py3gpp.nrPRBS import nrPRBS
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig
from py3gpp.nrPDSCHDMRS import PDSCHDMRSSyms

def nrPDSCHPTRS(carrier: nrCarrierConfig, cfg: nrPDSCHConfig):
    if cfg.EnablePTRS == 0:
        return []

    bwp_size = cfg.NRBSize * cfg.NSizeBWP

    # Generates first DMRS symbol (l0)
    n_scid = 0
    dmrs_occupied_syms = PDSCHDMRSSyms(cfg)
    cinit_dmrs = PDSCHPTRScinit(carrier.SymbolsPerSlot, carrier.NSlot, dmrs_occupied_syms[0], cfg.DMRS.NIDNSCID, n_scid)
    dmrs_prbs = nrPRBS(cinit_dmrs, bwp_size)
    dmrs_sym = nrSymbolModulate(dmrs_prbs, "QPSK")

    # Form PTRS symbols from DMRS l0 sequency
    ptrs_prb_set = PTRSPRBSet(cfg)

    ptrs_sym = np.array([dmrs_sym[x] for x in ptrs_prb_set])

    ptrs_occupied_syms = PDSCHPTRSSyms(carrier, cfg)

    return np.tile(ptrs_sym, len(ptrs_occupied_syms))


def PTRSPRBSet(cfg: nrPDSCHConfig):
    # Align with frequency offset based on DMRS type
    if cfg.DMRS.DMRSConfigurationType == 1:
        dmrs_ref_table = np.array([0, 2, 6, 8])
    else:
        dmrs_ref_table = np.array([0, 2, 4, 6])
    kRE_idx = int(cfg.PTRS.REOffset, 2)
    dmrsRef = dmrs_ref_table[kRE_idx]

    Nrb_mod_Kptrs = len(cfg.PRBSet) % cfg.PTRS.FrequencyDensity
    if Nrb_mod_Kptrs == 0:
        kRBref = cfg.RNTI % cfg.PTRS.FrequencyDensity
    else:
        kRBref = cfg.RNTI % Nrb_mod_Kptrs

    if cfg.DMRS.DMRSConfigurationType == 1:
        n_dmrs_per_re = 6
    else:
        n_dmrs_per_re = 4

    prb_set = np.array(cfg.PRBSet[kRBref::cfg.PTRS.FrequencyDensity])
    prb_set = (prb_set*n_dmrs_per_re)+dmrsRef//2

    return prb_set


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
            ptrs_cnt = 0
            continue

        if i in dmrs_syms:
            ptrs_cnt = 0
            continue

        ptrs_cnt += 1

        if ptrs_cnt == td:
            occupied_syms = np.append(occupied_syms, i)
            ptrs_cnt = 0

    return occupied_syms

def PDSCHPTRScinit(sps, n_slot, n_symb, NIDSCID, n_scid):
    return 2**17 * (sps * n_slot + n_symb + 1) * (2*NIDSCID + 1) + 2*NIDSCID + n_scid
