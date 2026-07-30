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
    if qm == 8:
        return '256QAM'
    assert False, f'modulation order = {qm} is not supported'
    return 0

class qam64_table():
    def __init__(self):
        self._table = np.zeros((4, 29), int)
        self._table[0,:] = np.arange(self._table.shape[1])
        self._table[1,:] = np.array(  [2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  4,  4,  4,  4,  4,  4,  4,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6])
        self._table[2,:] = np.array([120,157,193,251,308,379,449,526,602,679,340,378,434,490,553,616,658,438,466,517,567,616,666,719,772,822,873,910,948])
        self._table[3,:] = np.array([0.2344,0.3066,0.377,0.4902,0.6016,0.7402,0.877,1.0273,1.1758,1.3262,1.3281,1.4766,1.6953,1.9141,2.1602,2.4063,2.5703,2.5664,2.7305,3.0293,3.3223,3.6094,3.9023,4.2129,4.5234,4.8164,5.1152,5.332,5.5547])

    def Qm(self, mcs):
        return self._table[1,mcs]

    def Modulation(self, mcs):
        return qm_to_mod(self._table[1,mcs])
    
    def Rate(self, mcs):
        return self._table[2,mcs] / 1024

    def SpectralEfficiency(self, mcs):
        return self._table[3,mcs]

class qam64lowse_table():
    def __init__(self):
        self._table = np.zeros((4, 29), int)
        self._table[0,:] = np.arange(self._table.shape[1])
        self._table[1,:] = np.array(  [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,4,4,4,4,4,6,6,6,6,6,6,6,6])
        self._table[2,:] = np.array([30,40,50,64,78,99,120,157,193,251,308,379,449,526,602,340,378,434,490,553,616,438,466,517,567,616,666,719,772])
        self._table[3,:] = np.array([0.0586,0.0781,0.0977,0.125,0.1523,0.1934,0.2344,0.3066,0.377,0.4902,0.6016,0.7402,0.877,1.0273,1.1758,1.3281,1.4766,1.6953,1.9141,2.1602,2.4063,2.5664,2.7305,3.0293,3.3223,3.6094,3.9023,4.2129,4.5234])

    def Qm(self, mcs):
        return self._table[1,mcs]

    def Modulation(self, mcs):
        return qm_to_mod(self._table[1,mcs])

    def Rate(self, mcs):
        return self._table[2,mcs] / 1024

    def SpectralEfficiency(self, mcs):
        return self._table[3,mcs]

class qam256_table():
    def __init__(self):
        self._table = np.zeros((4, 28), int)
        self._table[0,:] = np.arange(self._table.shape[1])
        self._table[1,:] = np.array([2,2,2,2,2,4,4,4,4,4,4,6,6,6,6,6,6,6,6,6,8,8,8,8,8,8,8,8])
        self._table[2,:] = np.array([120,193,308,449,602,378,434,490,553,616,658,466,517,567,616,666,719,772,822,873,682.5,711,754,797,841,885,916.5,948])
        self._table[3,:] = np.array([0.2344,0.377,0.6016,0.877,1.1758,1.4766,1.6953,1.9141,2.1602,2.4063,2.5703,2.7305,3.0293,3.3223,3.6094,3.9023,4.2129,4.5234,4.8164,5.1152,5.332,5.5547,5.8906,6.2266,6.5703,6.9141,7.1602,7.4063])

    def Qm(self, mcs):
        return self._table[1,mcs]

    def Modulation(self, mcs):
        return qm_to_mod(self._table[1,mcs])

    def Rate(self, mcs):
        return self._table[2,mcs] / 1024

    def SpectralEfficiency(self, mcs):
        return self._table[3,mcs]

class pdsch_mcs_table_class():
    def __init__(self):
        self.QAM64Table = qam64_table()
        self.QAM64LowSETable = qam64lowse_table()
        self.QAM256Table = qam256_table()

def nrPDSCHMCSTables():
    return pdsch_mcs_table_class()

if __name__ == '__main__':
    table = nrPDSCHMCSTables().QAM64Table
    mcs = 0
    print(f'mcs = {mcs}, modulation = {table.Modulation(mcs)}, rate = {table.Rate(mcs)}')
    mcs = 16
    print(f'mcs = {mcs}, modulation = {table.Modulation(mcs)}, rate = {table.Rate(mcs)}')