# Ref: https://www.mathworks.com/help/5g/ref/nrlayermap.html
# Ref: TS 38.211 Sections 7.3.1.3

import numpy as np


def nrLayerMap(in_symbols, nLayers):

    # Check number of modulation symbols from either one or two codewords
    if isinstance(in_symbols, np.ndarray):
        if in_symbols.ndim == 2 and in_symbols.shape[1] == 1:
            in_symbols = [in_symbols]
            codewords = 1
        else:
            raise ValueError(
                "Input array should have a single column (shape Mx1).")
    elif isinstance(in_symbols, list):
        if len(in_symbols) == 1:
            if isinstance(in_symbols[0], np.ndarray) and in_symbols[0].ndim == 2 and in_symbols[0].shape[1] == 1:
                in_symbols = [in_symbols[0]]
                codewords = 1
            else:
                raise ValueError(
                    "Each array in the list should have a single column (shape Mx1).")
        elif len(in_symbols) == 2:
            if all(isinstance(arr, np.ndarray) and arr.ndim == 2 and arr.shape[1] == 1 for arr in in_symbols):
                codewords = 2
            else:
                raise ValueError(
                    "Each array in the list should have a single column (shape Mx1).")
        else:
            raise ValueError("Input list should contain either 1 or 2 arrays.")
    else:
        raise TypeError(
            "Input must be a numpy array or a list of numpy arrays.")
    
    # Check number of number of transmission layers
    if not isinstance(nLayers, int):
        raise TypeError("nLayers must be an integer.")
    if nLayers < 1 or nLayers > 8:
        raise ValueError("nLayers must be an integer between 1 and 8.")
    
    # Codeword to layer mapping (1 codewords)
    if codewords == 1:
        if nLayers == 1 or nLayers == 2 or nLayers == 3 or nLayers == 4:
            m = in_symbols[0].shape[0] / nLayers
            n = nLayers
            out = np.array([[m, n]])
        else:
            raise ValueError(
                "nLayers must be an integer between 1 to 4 for 1 codewords.")
    
    # Codeword to layer mapping (2 codewords)
    elif codewords == 2:
        if nLayers == 6 or nLayers == 8:
            m_one = in_symbols[0].shape[0] / (nLayers / 2)
            m_two = in_symbols[1].shape[0] / (nLayers / 2)
            n = nLayers
            if m_one == m_two:
                out = np.array([[m_one, n]])
            else:
                raise ValueError(
                    "in_symbols value does not match between codewords 1 and 2")
        elif nLayers == 5:
            m_one = in_symbols[0].shape[0] / 2
            m_two = in_symbols[1].shape[0] / 3
            n = nLayers
            if m_one == m_two:
                out = np.array([[m_one, n]])
            else:
                raise ValueError(
                    "in_symbols value does not match between codewords 1 and 2")
        elif nLayers == 7:
            m_one = in_symbols[0].shape[0] / 3
            m_two = in_symbols[1].shape[0] / 4
            n = nLayers
            if m_one == m_two:
                out = np.array([[m_one, n]])
            else:
                raise ValueError(
                    "in_symbols value does not match between codewords 1 and 2")
        else:
            raise ValueError(
                "nLayers must be an integer between 5 to 8 for 2 codewords.")
    return out


# # Example usage for one codeword (Array)
# out = nrLayerMap(np.ones((40, 1)), 4)
# print(out)

# # Example usage for one codeword (Array in List)
# out = nrLayerMap([np.ones((40, 1))], 4)
# print(out)

# # Example usage for two codeword (Array in List)
# out = nrLayerMap([np.ones((20, 1)), np.ones((30, 1))], 5)
# print(out)
