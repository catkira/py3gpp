import numpy as np
import sys


def nrCRCEncode(blk, poly, mask=0):
    if poly == "6":
        L = 6
        # fmt: off
        crc_coeffs = [6, 5, 0]
        # fmt: on
    elif poly == "11":
        L = 11
        # fmt: off
        crc_coeffs = [11, 10, 9, 5, 0]
        # fmt: on
    elif poly == "16":
        L = 16
        # fmt: off
        crc_coeffs = [16, 12, 5, 0]
        # fmt: on
    elif poly == "24A":
        L = 24
        # fmt: off
        crc_coeffs = [24, 23, 18, 17, 14, 11, 10, 7, 6, 5, 4, 3, 1, 0]
        # fmt: on
    elif poly == "24B":
        L = 24
        # fmt: off
        crc_coeffs = [24, 23, 6, 5, 1, 0]
        # fmt: on
    elif poly == "24C":
        L = 24
        # fmt: off
        crc_coeffs = [24, 23, 21, 20, 17, 15, 13, 12, 8, 4, 2, 1, 0]
        # fmt: on
    else:
        print("Error: invalid CRC polynomial specified!")
        sys.exit()
    blksrc = np.empty(len(blk) + L, "int")
    blksrc[: len(blk)] = blk

    # build crc_poly
    crc_poly = 0
    for crc_coeff in crc_coeffs:
        crc_poly += 2**crc_coeff

    # calculate crc
    crc = 0
    for bit in blk:
        if ((crc >> (L - 1)) & 1) != bit:
            crc = (crc << 1) ^ crc_poly
        else:
            crc = crc << 1
    crc ^= mask

    # append crc LSB first
    for i in range(L):
        blksrc[len(blk) + i] = (crc >> (L - i - 1)) & 1
    return blksrc


def test_nrCRCEncode():
    test = np.zeros(32)
    test[0] = 1
    result = nrCRCEncode(test, "24C")
    # fmt: off
    assert np.all(result == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
    # fmt: on
