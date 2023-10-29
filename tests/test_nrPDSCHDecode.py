import numpy as np
import pytest

from py3gpp.nrPDSCH import nrPDSCH
from py3gpp.nrPDSCHDecode import nrPDSCHDecode

@pytest.mark.parametrize('ncellid', [0, 1, 2, 3])
@pytest.mark.parametrize('modulation', ['16QAM', 'QPSK', 'BPSK'])
def test_run_nr_pdsch_combined(ncellid, modulation):
    modulation = [modulation]
    nlayers = 1
    rnti = 6143
    data = np.random.randint(0, 2, size=(1, 8000))
    txsym = nrPDSCH(data, modulation, nlayers, ncellid, rnti)
    rxbits = nrPDSCHDecode(txsym, modulation, ncellid, rnti)
    assert np.array_equal(data, np.round(rxbits<0).astype(int))