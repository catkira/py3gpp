import os
import sys
import itertools
import numpy as np
import pytest

from py3gpp.nrPDSCHDMRS import nrPDSCHDMRS
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

sys.path.append("test_data")

from test_data.pdsch import pdschdmrs_symbols_ref

def run_nr_pdschdmrs(cfg):
    carrier = nrCarrierConfig()
    carrier.SubcarrierSpacing = 120
    carrier.CyclicPrefix = 'normal'
    carrier.NSizeGrid = 132
    carrier.NStartGrid = 0

    pdsch_cfg = nrPDSCHConfig()
    pdsch_cfg.NSizeBWP = cfg['n_size_bwp']
    pdsch_cfg.NStartBWP = cfg['n_start_bwp']
    pdsch_cfg.MappingType = cfg['MappingType']
    pdsch_cfg.DMRS.DMRSTypeAPosition = cfg['DMRSTypeAPosition']
    pdsch_cfg.DMRS.DMRSLength = cfg['DMRSLength']
    pdsch_cfg.DMRS.DMRSAdditionalPosition = cfg['DMRSAdditionalPosition']
    pdsch_cfg.DMRS.DMRSConfigurationType = cfg['DMRSConfigurationType']
    pdsch_cfg.DMRS.NIDNSCID = cfg['NIDNSCID']
    pdsch_cfg.DMRS.NSCID = cfg['NSCID']
    pdsch_cfg.PRBSet = cfg['PRBSet']
    pdsch_cfg.SymbolAllocation = cfg['SymbolAllocation']

    pdschdmrs_syms = nrPDSCHDMRS(pdsch_cfg, carrier)

    # Cut neccesary part of reference indices
    # TODO: now it works only for 0 and 3 symbols. 1 and 2 quite tricky to cut...
    ref_data = pdschdmrs_symbols_ref
    first_idx = min(pdsch_cfg.PRBSet)*pdsch_cfg.NRBSize
    last_idx = (pdsch_cfg.DMRS.DMRSAdditionalPosition+1) * (max(pdsch_cfg.PRBSet)+1) * pdsch_cfg.NRBSize
    last_idx = last_idx//2
    ref_data = ref_data[first_idx:last_idx]

    pdschdmrs_syms = np.around(pdschdmrs_syms, 4)
    pdschdmrs_syms_ref = np.around(ref_data, 4)

    assert np.array_equal(pdschdmrs_syms, pdschdmrs_syms_ref)


@pytest.mark.parametrize('dmrs_add_pos', [0, 3])
def test_nr_pdschdmrs(dmrs_add_pos):
    cfg = {}
    cfg['n_size_bwp'] = 132
    cfg['n_start_bwp'] = 0
    cfg['MappingType'] = "A"
    cfg['DMRSTypeAPosition'] = 2
    cfg['DMRSLength'] = 1
    cfg['DMRSAdditionalPosition'] = dmrs_add_pos
    cfg['PRBSet'] = list(range(0, 132))
    cfg['SymbolAllocation'] = [2, 12]
    cfg['DMRSConfigurationType'] = 1
    cfg['NIDNSCID'] = 1
    cfg['NSCID'] = 0

    run_nr_pdschdmrs(cfg)
