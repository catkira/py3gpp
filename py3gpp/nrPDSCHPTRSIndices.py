
# 38.211

import numpy as np

from py3gpp.nrPDSCHPTRS import PDSCHPTRSSyms
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

def nrPDSCHPTRSIndices(carrier: nrCarrierConfig, cfg: nrPDSCHConfig):
    if cfg.EnablePTRS == 0:
        return np.array([])

    frame_begin = cfg.NRBSize * min(cfg.PRBSet)
    frame_end = cfg.NRBSize * (max(cfg.PRBSet)+1)
    frame_size = cfg.NRBSize * cfg.NSizeBWP

    # Align with frequency offset based on DMRS type
    if cfg.DMRS.DMRSConfigurationType == 1:
        kREref_table = [0, 2, 6, 8]
    else:
        kREref_table = [0, 1, 6, 7]
    kREref = kREref_table[int(cfg.PTRS.REOffset, 2)]

    Nrb_mod_Kptrs = len(cfg.PRBSet) % cfg.PTRS.FrequencyDensity
    if Nrb_mod_Kptrs == 0:
        kRBref = cfg.RNTI % cfg.PTRS.FrequencyDensity
    else:
        kRBref = cfg.RNTI % Nrb_mod_Kptrs
    kRBref *= cfg.NRBSize

    # Move to BWP offset and the rest frequency offsets
    ptrs_begin = frame_begin + kREref + kRBref

    # Calculate PTRS positions in every occupied symbol. Frequency position,
    # for every 2 or 4 RBs
    occupied_res = np.array(list(range(ptrs_begin, frame_end, (cfg.PTRS.FrequencyDensity*cfg.NRBSize))))

    # Calculates occupied symbols numbers. Time positions
    occupied_syms = PDSCHPTRSSyms(carrier, cfg)

    # Move PTRS indices to occupied symbols
    ptrs_indices = np.array([occupied_res+(sym*frame_size) for sym in occupied_syms])
    if len(ptrs_indices) > 0:
        ptrs_indices = np.concatenate(ptrs_indices, axis=None)

    return ptrs_indices
