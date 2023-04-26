import sys
import numpy as np
import pytest

from py3gpp.nrPDSCHPTRS import nrPDSCHPTRS
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

sys.path.append("test_data")

from test_data.pdsch import pdschptrs_symbols_ref

def run_nr_pdschptrs(cfg):
    carrier = nrCarrierConfig();
    carrier.SubcarrierSpacing = 120;
    carrier.CyclicPrefix = 'normal';
    carrier.NSizeGrid = 132;
    carrier.NStartGrid = 0;

    pdsch_cfg = nrPDSCHConfig();
    pdsch_cfg.NSizeBWP = cfg['n_size_bwp']
    pdsch_cfg.NStartBWP = cfg['n_start_bwp']
    pdsch_cfg.MappingType = cfg['MappingType']
    pdsch_cfg.DMRS.DMRSTypeAPosition = cfg['DMRSTypeAPosition']
    pdsch_cfg.DMRS.DMRSLength = cfg['DMRSLength']
    pdsch_cfg.DMRS.DMRSAdditionalPosition = cfg['DMRSAdditionalPosition']
    pdsch_cfg.DMRS.DMRSConfigurationType = cfg['DMRSConfigurationType']
    pdsch_cfg.DMRS.NIDNSCID = cfg['NIDNSCID']
    pdsch_cfg.DMRS.NSCID = cfg['NSCID']
    pdsch_cfg.RNTI = cfg['RNTI']
    pdsch_cfg.PRBSet = cfg['PRBSet']
    pdsch_cfg.SymbolAllocation = cfg['SymbolAllocation']

    pdsch_cfg.EnablePTRS = cfg['EnablePTRS']
    pdsch_cfg.PTRS.TimeDensity = cfg['PTRSTimeDensity']
    pdsch_cfg.PTRS.FrequencyDensity = cfg['PTRSFrequencyDensity']
    pdsch_cfg.PTRS.REOffset = cfg['PTRSREOffset']

    pdschptrs_syms = nrPDSCHPTRS(carrier, pdsch_cfg)
    pdschptrs_syms = np.around(pdschptrs_syms, 4)

    ref_data = pdschptrs_symbols_ref
    ref_data = np.around(ref_data, 4)

    assert np.array_equal(pdschptrs_syms, ref_data)


def test_nr_pdschptrs():
    cfg = {}
    cfg['n_size_bwp'] = 132
    cfg['n_start_bwp'] = 0
    cfg['MappingType'] = "A"
    cfg['DMRSTypeAPosition'] = 3
    cfg['DMRSLength'] = 1
    cfg['DMRSAdditionalPosition'] = 3
    cfg['PRBSet'] = list(range(0, 132))
    cfg['SymbolAllocation'] = [2, 12]
    cfg['DMRSConfigurationType'] = 2
    cfg['NIDNSCID'] = 1
    cfg['NSCID'] = 0
    cfg['RNTI'] = 1
    cfg['EnablePTRS'] = 1
    cfg['PTRSTimeDensity'] = 2
    cfg['PTRSFrequencyDensity'] = 4
    cfg['PTRSREOffset'] = '11'

    run_nr_pdschptrs(cfg)
