# Ref: https://ch.mathworks.com/help/5g/ref/nrtbs.html#d124e53763
# Ref: TS 38.214 Sections 5.1.3.2

import numpy as np
import math


def nrTBS(mod, nlayers, nPRB, NREPerPRB, tcr, xOh=0, tbScaling=1):

    ### Pre-defined table ###

    modulation_schemes = {
        'pi/2-BPSK': 1,
        'QPSK': 2,
        '16QAM': 4,
        '64QAM': 6,
        '256QAM': 8,
        '1024QAM': 10
    }

    tbs_values = [
        24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160,
        168, 176, 184, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384,
        408, 432, 456, 480, 504, 528, 552, 576, 608, 640, 672, 704, 736, 768, 808, 848,
        888, 928, 984, 1032, 1064, 1128, 1160, 1192, 1224, 1256, 1288, 1320, 1352, 1416,
        1480, 1544, 1608, 1672, 1736, 1800, 1864, 1928, 2024, 2088, 2152, 2216, 2280,
        2408, 2472, 2536, 2600, 2664, 2728, 2792, 2856, 2976, 3104, 3240, 3368, 3496,
        3624, 3752, 3824
    ]

    ### Input check ###

    # nlayers
    if not (1 <= nlayers <= 8):
        raise ValueError("nlayers must be an integer between 1 and 8")

    # nPRB
    if nPRB < 0:
        raise ValueError("nPRB must be a nonnegative integer")

    # NREPerPRB
    if NREPerPRB < 0:
        raise ValueError("NREPerPRB must be a nonnegative integer")

    # xOh
    if not isinstance(xOh, int) or xOh < 0:
        raise ValueError("xOh must be a nonnegative integer")

    # tbScaling
    if isinstance(tbScaling, (int, float)):
        if not (0 < tbScaling <= 1):
            raise ValueError("tbScaling must be a scalar in the range (0, 1]")
    elif isinstance(tbScaling, (list, tuple)) and len(tbScaling) == 2:
        if not (0 < tbScaling[0] <= 1) or not (0 < tbScaling[1] <= 1):
            raise ValueError(
                "Each element in tbScaling must be in the range (0, 1]")
    else:
        raise ValueError("Invalid type or format for tbScaling")

    # tcr
    if isinstance(tcr, (float, int)):
        tcr = [tcr]
        if not (0 <= tcr[0] <= 1):
            raise ValueError("tcr must be a scalar between 0 and 1")
    elif isinstance(tcr, (list, tuple)):
        if len(tcr) != len(mod):
            raise ValueError(
                "The number of elements in 'tcr' must match the number of codewords")
        for t in tcr:
            if not (0 <= t <= 1):
                raise ValueError(
                    "Each element in 'tcr' must be between 0 and 1")
    else:
        raise ValueError(
            "Invalid type for 'tcr'. It must be a scalar, list, or tuple")

    # mod
    if isinstance(mod, (str, list, tuple)):
        if isinstance(mod, str):
            mod = [mod]
        if len(mod) <= 2:
            if all(m in modulation_schemes for m in mod):
                bits_per_symbol = [modulation_schemes[m] for m in mod]
            else:
                raise ValueError("Invalid modulation scheme(s) in the input")
        else:
            raise ValueError(
                "Input 'mod' must be a single valid modulation or a list/tuple of 2 valid modulations")
    else:
        raise ValueError(
            "Invalid type for 'mod'. It must be a single valid modulation or a list/tuple of 2 valid modulations")

    ### Calculate N Info for each codeword ###

    n_info = []
    for i in range(len(mod)):
        n_re = min(156, (NREPerPRB - xOh)) * \
            (nPRB // len(mod))  # Divide nPRB into equal parts
        n_info.append(tbScaling * n_re * tcr[i] * bits_per_symbol[i] * nlayers)

    tbs = []
    for i in range(len(n_info)):
        # Check conditions to set tbs to 0
        if NREPerPRB == 0 or nPRB == 0 or NREPerPRB < xOh:
            tbs.append(0)
        else:
            # Calculate DL TBS for each codeword
            if n_info[i] <= 3824:
                n = max(3, math.floor(abs(math.log2(n_info[i]) - 6)))
                n_info_ = max(24, (2**n) * math.floor(abs(n_info[i] / (2**n))))
                closest_tbs = min(filter(lambda tbs: tbs >= n_info_,
                                         tbs_values), key=lambda tbs: abs(tbs - n_info_))
                n_info[i] = max(n_info_, closest_tbs)
            else:
                n = math.floor(abs(math.log2(n_info[i] - 24) - 5))
                n_info_ = max(3840, (2**n) * round((n_info[i] - 24) / (2**n)))
                if tcr[i] <= 0.25:
                    c = math.ceil(abs((n_info_ + 24) / (3816)))
                    n_info[i] = (
                        8 * c * (math.ceil(abs((n_info_ + 24) / (8 * c))))) - 24
                else:
                    if n_info_ > 8424:
                        c = math.ceil(abs((n_info_ + 24) / (8424)))
                        n_info[i] = (
                            8 * c * (math.ceil(abs((n_info_ + 24) / (8 * c))))) - 24
                    else:
                        n_info[i] = (
                            8 * (math.ceil(abs((n_info_ + 24) / (8))))) - 24

            tbs.append(int(n_info[i]))

    ### Input check ###
    if len(tbs) == 1:
        tbs = int(tbs[0])  # Convert to integer
    else:
        tbs = np.array(tbs)  # Convert to NumPy array

    return tbs


# # Example usage for one codeword
# modulation = '16QAM'
# nlayers = 4
# nPRB = 52
# NREPerPRB = 120
# tcr = 0.48
# xOh = 6
# tbScaling = 0.25
# tbs = nrTBS(modulation, nlayers, nPRB, NREPerPRB, tcr, xOh, tbScaling)
# print(f'TBS for One Codeword: {tbs}')

# # Example usage for two codewords
# modulation = ['QPSK', '64QAM']
# nlayers = 8
# nPRB = 106
# NREPerPRB = 100
# tcr = [0.3701, 0.4277]
# xOh = 0
# tbScaling = 1
# tbs = nrTBS(modulation, nlayers, nPRB, NREPerPRB, tcr, xOh, tbScaling)
# print(f'TBS for Two Codewords: {tbs}')
