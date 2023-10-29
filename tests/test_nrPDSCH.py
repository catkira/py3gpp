
import sys
import itertools
import numpy as np
import pytest

from py3gpp.nrPDSCH import nrPDSCH

sys.path.append("test_data")

from test_data.pdsch import pdsch_symbols_ref, pdsch_bits_ref

def run_nr_pdsch(cws, modulation, nlayers, nid, nrnti):
    pdsch_syms = nrPDSCH(cws, modulation, nlayers, nid, nrnti)
    pdsch_syms = np.around(pdsch_syms, 4)

    assert np.array_equal(pdsch_syms[0], pdsch_symbols_ref)

def test_run_nr_pdsch():
    run_nr_pdsch([pdsch_bits_ref], ["64QAM"], 1, 0, 0)

if __name__ == '__main__':
    run_nr_pdsch([pdsch_bits_ref], ["64QAM"], 1, 0, 0)