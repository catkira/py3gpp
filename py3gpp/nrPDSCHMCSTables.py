import numpy as np

def qm_to_mod(qm):
    if qm == 1:
        return 'BPSK'
    if qm == 2:
        return 'QPSK'
    if qm == 4:
        return '16QAM'
    if qm == 6:
        return '64QAM'
    assert False, f'modulation order = {qm} is not supported'
    return 0

class qam16_table():
    def __init__(self):
        self._table = np.zeros((4, 29), int)
        self._table[0,:] = np.arange(self._table.shape[1])
        self._table[1,:] = np.array(  [2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  4,  4,  4,  4,  4,  4,  4,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6])
        self._table[2,:] = np.array([120,157,193,251,308,379,449,526,602,679,340,378,434,490,553,616,658,438,466,517,567,616,666,719,772,822,873,910,948])

    def Qm(self, mcs):
        return self._table[1,mcs]

    def Modulation(self, mcs):
        return qm_to_mod(self._table[1,mcs])
    
    def Rate(self, mcs):
        return self._table[2,mcs] / 1024


class pdsch_mcs_table_class():
    def __init__(self):
        self.QAM64Table = qam16_table()

def nrPDSCHMCSTables():
    return pdsch_mcs_table_class()

if __name__ == '__main__':
    table = nrPDSCHMCSTables().QAM64Table
    mcs = 0
    print(f'mcs = {mcs}, modulation = {table.Modulation(mcs)}, rate = {table.Rate(mcs)}')
    mcs = 16
    print(f'mcs = {mcs}, modulation = {table.Modulation(mcs)}, rate = {table.Rate(mcs)}')