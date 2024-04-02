import numpy as np

from py3gpp.nrPDSCHMCSTables import nrPDSCHMCSTables

def test_nrPDSCHMCSTables():
    table = nrPDSCHMCSTables().QAM64Table
    mcs = 0
    assert table.Modulation(mcs) == 'QPSK'
    assert table.Qm(mcs) == 2
    assert table.Rate(mcs) == 120 / 1024

    mcs = 15
    assert table.Modulation(mcs) == '16QAM'
    assert table.Qm(mcs) == 4
    assert table.Rate(mcs) == 616 / 1024

    mcs = 16
    assert table.Modulation(mcs) == '16QAM'
    assert table.Qm(mcs) == 4
    assert table.Rate(mcs) == 658 / 1024

if __name__ == '__main__':
    test_nrPDSCHMCSTables()