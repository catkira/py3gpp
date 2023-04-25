
# 38.211

import numpy as np

from py3gpp.nrPRBS import nrPRBS
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

def nrPDSCHDMRS(cfg: nrPDSCHConfig, carrier: nrCarrierConfig):
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
    dmrs_syms = np.array([])
    for n_symb in occupied_syms:
        cinit_dmrs = PDSCHDMRScinit(carrier.SymbolsPerSlot, carrier.NSlot, n_symb, cfg.DMRS.NIDNSCID, n_scid)
        dmrs_prbs = nrPRBS(cinit_dmrs, dmrs_size)

        # Cut PRBS sequency
        dmrs_prbs = dmrs_prbs[dmrs_begin:dmrs_end]
        dmrs_syms = np.append(dmrs_syms, nrSymbolModulate(dmrs_prbs, "QPSK"))

    return dmrs_syms

# LUT for DMRS occupied symbols positions
def PDSCHDMRSSyms(cfg: nrPDSCHConfig):
    l1 = 11
    typeA_pos = cfg.DMRS.DMRSTypeAPosition
    sym_alloc = cfg.SymbolAllocation[1]
    add_pos = cfg.DMRS.DMRSAdditionalPosition
    dmrs_len = cfg.DMRS.DMRSLength

    occupied_syms = np.array([], dtype=int)
    occupied_syms = np.append(occupied_syms, typeA_pos)

    if sym_alloc in [8, 9]:
        occupied_syms = np.append(occupied_syms, 7)
    elif sym_alloc in [10, 11]:
        if add_pos == 1:
            occupied_syms = np.append(occupied_syms, 9)
        elif add_pos == 2 or add_pos == 3:
            occupied_syms = np.append(occupied_syms, [6, 9])
    elif sym_alloc == 12:
        if add_pos == 1:
            occupied_syms = np.append(occupied_syms, 11)
        elif add_pos == 2:
            occupied_syms = np.append(occupied_syms, [7, 11])
        elif add_pos == 3:
            occupied_syms = np.append(occupied_syms, [5, 8, 11])
    elif sym_alloc in [13, 14]:
        if add_pos == 1:
            occupied_syms = np.append(occupied_syms, l1)
        elif add_pos == 2:
            occupied_syms = np.append(occupied_syms, [7, 11])
        elif add_pos == 3:
            occupied_syms = np.append(occupied_syms, [5, 8, 11])

    if dmrs_len == 2:
        occupied_syms = [x+1 for x in occupied_syms]

    return occupied_syms

def PDSCHDMRScinit(sps, n_slot, n_symb, NIDSCID, n_scid):
    return 2**17 * (sps * n_slot + n_symb + 1) * (2*NIDSCID + 1) + 2*NIDSCID + n_scid