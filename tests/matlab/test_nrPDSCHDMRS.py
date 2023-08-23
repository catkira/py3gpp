import matlab.engine
import os
import itertools
import numpy as np
import pytest

from py3gpp.nrPDSCHDMRS import nrPDSCHDMRS
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

def run_nr_pdschdmrs(cfg, eng):
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
    pdsch_cfg.PRBSet = cfg['PRBSet']
    pdsch_cfg.SymbolAllocation = cfg['SymbolAllocation']

    pdschdmrs_syms = nrPDSCHDMRS(pdsch_cfg, carrier)

    [pdschdmrs_syms_ref, _] = eng.gen_pdschdmrs(cfg, nargout=2)
    pdschdmrs_syms_ref = np.array(list(itertools.chain(*pdschdmrs_syms_ref)))

    pdschdmrs_syms = np.around(pdschdmrs_syms, 4)
    pdschdmrs_syms_ref = np.around(pdschdmrs_syms_ref, 4)

    assert np.array_equal(pdschdmrs_syms, pdschdmrs_syms_ref)

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize('typeA_pos', [2, 3])
@pytest.mark.parametrize('symb_alloc', [[2, 12]])
@pytest.mark.parametrize('dmrs_add_pos', [0, 1, 2, 3])
@pytest.mark.parametrize('PRBSet', [list(range(0, 132)), list(range(60, 132)), list(range(30, 60))])
@pytest.mark.parametrize('dmrs_cfg_type', [1, 2])
def test_nr_pdschdmrs(symb_alloc, dmrs_add_pos, typeA_pos, PRBSet, dmrs_cfg_type, eng):
    eng.cd(os.path.dirname(__file__))

    cfg = {}
    cfg['n_size_bwp'] = 132
    cfg['n_start_bwp'] = 0
    cfg['MappingType'] = "A"
    cfg['DMRSTypeAPosition'] = typeA_pos
    cfg['DMRSLength'] = 1
    cfg['DMRSAdditionalPosition'] = dmrs_add_pos
    cfg['PRBSet'] = PRBSet
    cfg['SymbolAllocation'] = symb_alloc
    cfg['DMRSConfigurationType'] = dmrs_cfg_type
    cfg['NIDNSCID'] = 1
    cfg['NSCID'] = 0
    cfg['EnablePTRS'] = 0

    run_nr_pdschdmrs(cfg, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    test_nr_pdschdmrs([2, 12], 1, 2, list(range(2, 130)), 2, _eng)
    _eng.quit()
