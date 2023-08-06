import numpy as np

def nrDLSCHInfo(tbs, tcr):
    assert tbs >= 0
    assert type(tbs) == int
    assert tcr > 0 and tcr < 1

    bg_info = getBGNInfo(tbs, tcr)
    cb_info = getCBSInfo(bg_info["B"], bg_info["BGN"])

    # Get number of bits (including filler bits) to be encoded by LDPC encoder
    if bg_info["BGN"] == 1:
        N = 66*cb_info["Zc"]
    else:
        N = 50*cb_info["Zc"]

    # Combine information into the output structure
    info = dict()
    info["CRC"]      = bg_info["CRC"]  # CRC polynomial
    info["L"]        = bg_info["L"]    # Number of CRC bits
    info["BGN"]      = bg_info["BGN"]  # Base graph number
    info["C"]        = cb_info["C"]    # Number of code block segments
    info["Lcb"]      = cb_info["Lcb"]  # Number of parity bits per code block
    info["F"]        = cb_info["F"]    # Number of <NULL> filler bits per code block
    info["Zc"]       = cb_info["Zc"]   # Selected lifting size
    info["K"]        = cb_info["K"]    # Number of bits per code block after CBS
    info["N"]        = N              # Number of bits per code block after LDPC coding

    # Modify the output fields if tbs is empty or zero
    if tbs is None:
        info["L"]  = 0
        info["F"]  = 0
        info["Zc"] = 2
        info["K"]  = 0
        info["N"]  = 0

    return info


def getBGNInfo(A, R):
    if A <= 292 or (A <= 3824 and R <= 0.67) or R <= 0.25:
        bgn = 2
    else:
        bgn = 1

    if A > 3824:
        L   = 24
        crc = '24A'
    else:
        L   = 16
        crc = '16'

    info = dict()
    info["BGN"] = bgn
    info["B"]   = A + L
    info["L"]   = L
    info["CRC"] = crc

    return info


def getCBSInfo(B, bgn):
    if bgn == 1:
        Kcb = 8448
    else:
        Kcb = 3840

    # Get number of code blocks and length of CB-CRC coded block
    if B <= Kcb:
        L = 0
        C = 1
        Bd = B
    else:
        L = 24 # Length of the CRC bits attached to each code block
        C = np.ceil(B/(Kcb-L)).astype(int)
        Bd = B+C*L

    # Obtain the number of bits per code block (excluding CB-CRC bits)
    cbz = np.ceil(B/C).astype(int)

    # Get number of bits in each code block (excluding filler bits)
    Kd = np.ceil(Bd/C)

    # Find the minimum value of Z in all sets of lifting sizes in 38.212
    # Table 5.3.2-1, denoted as Zc, such that Kb*Zc>=Kd
    if bgn == 1:
        Kb = 22
    else:
        if B > 640:
            Kb = 10
        elif B > 560:
            Kb = 9
        elif B > 192:
            Kb = 8
        else:
            Kb = 6

    # Zlist = [2:16 18:2:32 36:4:64 72:8:128 144:16:256 288:32:384];
    Zlist = []
    Zlist += list(range(2, 17))
    Zlist += list(range(18, 33, 2))
    Zlist += list(range(36, 65, 4))
    Zlist += list(range(72, 129, 8))
    Zlist += list(range(144, 257, 16))
    Zlist += list(range(288, 385, 32))

    # Zc = min(Zlist(Kb*Zlist >= Kd));
    # Zc = []
    # for x in Zlist:
    #     if Kb*x >= Kd:
    #         Zc.append(x)
    # Zc = min(Zc)
    Zc = min([x for x in Zlist if (Kb*x >= Kd)])

    # Get number of bits (including <NULL> filler bits) to be input to the LDPC encoder
    if bgn == 1:
        K = 22*Zc
    else:
        K = 10*Zc

    info = dict()
    info["C"]   = C     # Number of code block segments
    info["CBZ"] = cbz   # Number of bits in each code block (excluding CB-CRC bits and filler bits)
    info["Lcb"] = L     # Number of parity bits in each code block
    info["F"]   = K-Kd  # Number of filler bits in each code block
    info["K"]   = K     # Number of bits in each code block (including CB-CRC bits and filler bits)
    info["Zc"]  = Zc    # Selected lifting size
    info["Z"]   = Zlist # Full lifting size set

    return info
