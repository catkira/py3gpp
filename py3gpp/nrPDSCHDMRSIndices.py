
# 38.211

import numpy as np

from py3gpp.nrPDSCHDMRS import PDSCHDMRSSyms
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig

def nrPDSCHDMRSIndices(cfg: nrPDSCHConfig):
    frame_begin = cfg.NRBSize * min(cfg.PRBSet)
    frame_end = cfg.NRBSize * (max(cfg.PRBSet)+1)
    frame_size = cfg.NRBSize * cfg.NSizeBWP

    # Single frame DMRS positions
    dmrs_full_range = np.array(list(range(frame_begin, frame_end)))

    # Calculate DMRS positions in every occupied symbol. Frequency position
    if cfg.DMRS.DMRSConfigurationType == 1:
        # Takes every 2nd symbol
        occupied_res = dmrs_full_range[::2]
    elif cfg.DMRS.DMRSConfigurationType == 2:
        # Takes every 4th couple of symbols
        occupied_res = dmrs_full_range.reshape(-1, 2)[::3].ravel()

    # Calculates occupied symbols numbers. Time positions
    occupied_syms = PDSCHDMRSSyms(cfg)

    dmrs_indices = np.array([])
    for idx, sym in enumerate(occupied_syms):
        sym_offset = sym*frame_size
        dmrs_indices = np.append(dmrs_indices, (occupied_res + sym_offset))

    return dmrs_indices
