from .helper import _calc_gold

# v: scrambling sequence phase, 0..7
# n: number of elements in output sequence
def nrPBCHPRBS(ncellid, v, n):
    seq = _calc_gold(ncellid, n + v * n)
    return seq[v * n :][:n]
