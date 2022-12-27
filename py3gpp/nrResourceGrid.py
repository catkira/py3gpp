import numpy as np


def nrResourceGrid(carrier, p=1):
    SymbolsPerSlot = 14
    if p == 1:
        grid = np.zeros((12 * carrier.NSizeGrid, SymbolsPerSlot), "complex")
    else:
        grid = np.zeros((12 * carrier.NSizeGrid, SymbolsPerSlot, p), "complex")
    return grid
