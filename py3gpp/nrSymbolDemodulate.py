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
    output = np.empty(0, "float")

    for symbol in input:
        if mod == "BPSK":
            output = np.append(output, np.real(symbol) + np.imag(symbol))
        elif mod == "QPSK":
            output = np.append(output, np.real(symbol))
            output = np.append(output, np.imag(symbol))
        elif mod == "16QAM":
            output = np.append(output, np.real(symbol))
            output = np.append(output, np.imag(symbol))
            output = np.append(output, -(np.abs(np.real(symbol)) - 2 / np.sqrt(10)))
            output = np.append(output, -(np.abs(np.imag(symbol)) - 2 / np.sqrt(10)))

    if DecisionType == "soft":
        output /= nVar / np.exp(1)
        if mod == "16QAM":
            output /= 2
    else:
        output = (output < 0).astype(int)
    return output
