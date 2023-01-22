import numpy as np

def _calc_m_seq(N, c, taps, seq_len = None):
    if seq_len is None:
        seq_len = 2**N - 1
    m = np.zeros(seq_len, "int32")  # m-sequence
    assert len(c) == N, "c has wrong length"
    m[:N] = c
    for i in np.arange(0, seq_len - N):
        m[i + N] = np.sum(np.take(m, i + taps)) % 2
    return m


# TS 38.211 Section 5.2.1
def _calc_gold(c_init, length):
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
