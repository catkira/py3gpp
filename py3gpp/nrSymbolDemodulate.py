import numpy as np

# 16QAM constellation:
#                Q
#  1011    1001  |   0001  0011
#  1010    1000  |   0000  0010
# ---------------------------------> I
#  1110    1100  |   0100  0110
#  1111    1101  |   0101  0111
def _16QAM_table():
    table = np.empty(16, "complex")
    QAM16_LEVEL_1 = 1 / np.sqrt(10)
    QAM16_LEVEL_2 = 3 / np.sqrt(10)
    table[0] = QAM16_LEVEL_1 + 1j * QAM16_LEVEL_1
    table[1] = QAM16_LEVEL_1 + 1j * QAM16_LEVEL_2
    table[2] = QAM16_LEVEL_2 + 1j * QAM16_LEVEL_1
    table[3] = QAM16_LEVEL_2 + 1j * QAM16_LEVEL_2
    table[4] = QAM16_LEVEL_1 - 1j * QAM16_LEVEL_1
    table[5] = QAM16_LEVEL_1 - 1j * QAM16_LEVEL_2
    table[6] = QAM16_LEVEL_2 - 1j * QAM16_LEVEL_1
    table[7] = QAM16_LEVEL_2 - 1j * QAM16_LEVEL_2
    table[8] = -QAM16_LEVEL_1 + 1j * QAM16_LEVEL_1
    table[9] = -QAM16_LEVEL_1 + 1j * QAM16_LEVEL_2
    table[10] = -QAM16_LEVEL_2 + 1j * QAM16_LEVEL_1
    table[11] = -QAM16_LEVEL_2 + 1j * QAM16_LEVEL_2
    table[12] = -QAM16_LEVEL_1 - 1j * QAM16_LEVEL_1
    table[13] = -QAM16_LEVEL_1 - 1j * QAM16_LEVEL_2
    table[14] = -QAM16_LEVEL_2 - 1j * QAM16_LEVEL_1
    table[15] = -QAM16_LEVEL_2 - 1j * QAM16_LEVEL_2
    return table


def nrSymbolDemodulate(input, mod, nVar=1e-10, DecisionType="soft"):
    r_i = np.real(input)
    r_q = np.imag(input)
    if mod == "BPSK":
        output = r_i + r_q
        K = 1
    elif mod == "QPSK":
        output = np.zeros(len(input) * 2, dtype="float")
        output[0::2] = r_i
        output[1::2] = r_q
        K = 1
    elif mod == "16QAM":
        d = 1 / np.sqrt(10)
        output = np.zeros(len(input) * 4, dtype="float")
        output[0::4] = r_i
        output[1::4] = r_q
        output[2::4] = 2 * d - np.abs(r_i)
        output[3::4] = 2 * d - np.abs(r_q)
        K = 4 * d
    elif mod == "64QAM":
        d = 1 / np.sqrt(42)
        output = np.zeros(len(input) * 6, dtype="float")
        output[0::6] = r_i
        output[1::6] = r_q
        output[2::6] = 4 * d - np.abs(r_i)
        output[3::6] = 4 * d - np.abs(r_q)
        output[4::6] = 2 * d - np.abs(4 * d - np.abs(r_i))
        output[5::6] = 2 * d - np.abs(4 * d - np.abs(r_q))
        K = 4 * d
    elif mod == "256QAM":
        d = 1 / np.sqrt(170)
        output = np.zeros(len(input) * 8, dtype="float")
        output[0::8] = r_i
        output[1::8] = r_q
        output[2::8] = 8 * d - np.abs(r_i)
        output[3::8] = 8 * d - np.abs(r_q)
        output[4::8] = 4 * d - np.abs(8 * d - np.abs(r_i))
        output[5::8] = 4 * d - np.abs(8 * d - np.abs(r_q))
        output[6::8] = 2 * d - np.abs(4 * d - np.abs(8 * d - np.abs(r_i)))
        output[7::8] = 2 * d - np.abs(4 * d - np.abs(8 * d - np.abs(r_q)))
        K = 4 * d
    else:
        raise NotImplementedError(mod)

    if DecisionType == "soft":
        output *= K / nVar
    else:
        output = (output < 0).astype(int)
    return output
