import numpy as np


def nrExtractResources(ind, grid):
    return grid.ravel(order="F")[ind]
