
from .helper import _calc_m_seq
import numpy as np

# TS 38.211 Section 5.2.1
def nrPRBS(c_init, length):
    assert length > 0

    N = 31

    c_0 = np.zeros(N)
    c_0[0] = 1
    c_1 = np.zeros(N)
    for i in range(N):
        c_1[i] = (c_init>>i) & 1

    Nc = 1600
    seq_len = length + Nc
    mseq_0 = _calc_m_seq(N, c_0, [0, 3], seq_len)
    mseq_1 = _calc_m_seq(N, c_1, [0, 1, 2, 3], seq_len)

    gold_seq = (mseq_0 + mseq_1) % 2
    gold_seq = np.roll(gold_seq, -Nc)
    return gold_seq[: length]
