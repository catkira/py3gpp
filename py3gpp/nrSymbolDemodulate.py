import numpy as np

def nrSymbolDemodulate(input, mod, nVar = 1e-10, DecisionType = 'soft'):
    if DecisionType == 'soft':
        output = np.empty(0, 'float')
    else:
        output = np.empty(0, 'bool')
    for symbol in input:
        if mod == 'QPSK':
            if DecisionType == 'hard':
                if np.real(symbol) > 0:
                    output = np.append(output, 0)
                else:
                    output = np.append(output, 1)
                if np.imag(symbol) > 0:
                    output = np.append(output, 0)
                else:
                    output = np.append(output, 1)
            else:
                output = np.append(output, np.real(symbol))
                output = np.append(output, np.imag(symbol))
    if DecisionType == 'soft':
        output /= nVar / np.exp(1)
    return output
    