import numpy as np

from py3gpp.nrPDSCHDMRS import PDSCHDMRSSyms
from py3gpp.configs.nrPDSCHConfig import nrPDSCHConfig
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

def nrPDSCHIndices(carrier: nrCarrierConfig, pdsch: nrPDSCHConfig):
    frame_begin = pdsch.NRBSize * (min(pdsch.PRBSet))
    frame_end = pdsch.NRBSize * (max(pdsch.PRBSet) + 1)

    occupied_syms = np.arange(pdsch.SymbolAllocation[0], pdsch.SymbolAllocation[1])
    indices = np.repeat(np.expand_dims(np.arange(frame_begin, frame_end), 0), occupied_syms.shape[0], axis = 0)
    for i in range(indices.shape[0]):
        indices[i, :] += carrier.NSizeGrid * pdsch.NRBSize * i + pdsch.NStartBWP * pdsch.NRBSize
    indices = np.delete(indices, PDSCHDMRSSyms(pdsch), axis = 0)
    return indices.ravel()


if __name__ == '__main__':
    pdsch = nrPDSCHConfig()
    carrier = nrCarrierConfig()
    carrier.NSizeGrid = 52
    pdsch.NSizeBWP = 25
    pdsch.NStartBWP = 10
    pdsch.PRBSet = np.arange(pdsch.NSizeBWP)
    indices = nrPDSCHIndices(carrier, pdsch)
    print(indices.shape)
    print(indices)