import numpy as np

# fmt: off
frozen_pos_table = np.array([0, 1, 2, 4, 8, 16, 32, 3, 5, 64, 9, 6, 17, 10, 18, 128, 12, 33, 65, 20, 256, 34, 24, 36,
    7, 129, 66, 512, 11, 40, 68, 130, 19, 13, 48, 14, 72, 257, 21, 132, 35, 258, 26, 513, 80, 37, 25, 22, 136, 260,
    264, 38, 514, 96, 67, 41, 144, 28, 69, 42, 516, 49, 74, 272, 160, 520, 288, 528, 192, 544, 70, 44, 131, 81, 50,
    73, 15, 320, 133, 52, 23, 134, 384, 76, 137, 82, 56, 27, 97, 39, 259, 84, 138, 145, 261, 29, 43, 98, 515, 88, 140,
    30, 146, 71, 262, 265, 161, 576, 45, 100, 640, 51, 148, 46, 75, 266, 273, 517, 104, 162, 53, 193, 152, 77, 164,
    768, 268, 274, 518, 54, 83, 57, 521, 112, 135, 78, 289, 194, 85, 276, 522, 58, 168, 139, 99, 86, 60, 280, 89, 290,
    529, 524, 196, 141, 101, 147, 176, 142, 530, 321, 31, 200, 90, 545, 292, 322, 532, 263, 149, 102, 105, 304, 296,
    163, 92, 47, 267, 385, 546, 324, 208, 386, 150, 153, 165, 106, 55, 328, 536, 577, 548, 113, 154, 79, 269, 108, 578,
    224, 166, 519, 552, 195, 270, 641, 523, 275, 580, 291, 59, 169, 560, 114, 277, 156, 87, 197, 116, 170, 61, 531,
    525, 642, 281, 278, 526, 177, 293, 388, 91, 584, 769, 198, 172, 120, 201, 336, 62, 282, 143, 103, 178, 294, 93,
    644, 202, 592, 323, 392, 297, 770, 107, 180, 151, 209, 284, 648, 94, 204, 298, 400, 608, 352, 325, 533, 155, 210,
    305, 547, 300, 109, 184, 534, 537, 115, 167, 225, 326, 306, 772, 157, 656, 329, 110, 117, 212, 171, 776, 330, 226,
    549, 538, 387, 308, 216, 416, 271, 279, 158, 337, 550, 672, 118, 332, 579, 540, 389, 173, 121, 553, 199, 784, 179,
    228, 338, 312, 704, 390, 174, 554, 581, 393, 283, 122, 448, 353, 561, 203, 63, 340, 394, 527, 582, 556, 181, 295,
    285, 232, 124, 205, 182, 643, 562, 286, 585, 299, 354, 211, 401, 185, 396, 344, 586, 645, 593, 535, 240, 206, 95,
    327, 564, 800, 402, 356, 307, 301, 417, 213, 568, 832, 588, 186, 646, 404, 227, 896, 594, 418, 302, 649, 771, 360,
    539, 111, 331, 214, 309, 188, 449, 217, 408, 609, 596, 551, 650, 229, 159, 420, 310, 541, 773, 610, 657, 333, 119,
    600, 339, 218, 368, 652, 230, 391, 313, 450, 542, 334, 233, 555, 774, 175, 123, 658, 612, 341, 777, 220, 314, 424,
    395, 673, 583, 355, 287, 183, 234, 125, 557, 660, 616, 342, 316, 241, 778, 563, 345, 452, 397, 403, 207, 674, 558,
    785, 432, 357, 187, 236, 664, 624, 587, 780, 705, 126, 242, 565, 398, 346, 456, 358, 405, 303, 569, 244, 595, 189,
    566, 676, 361, 706, 589, 215, 786, 647, 348, 419, 406, 464, 680, 801, 362, 590, 409, 570, 788, 597, 572, 219, 311,
    708, 598, 601, 651, 421, 792, 802, 611, 602, 410, 231, 688, 653, 248, 369, 190, 364, 654, 659, 335, 480, 315, 221,
    370, 613, 422, 425, 451, 614, 543, 235, 412, 343, 372, 775, 317, 222, 426, 453, 237, 559, 833, 804, 712, 834, 661,
    808, 779, 617, 604, 433, 720, 816, 836, 347, 897, 243, 662, 454, 318, 675, 618, 898, 781, 376, 428, 665, 736, 567,
    840, 625, 238, 359, 457, 399, 787, 591, 678, 434, 677, 349, 245, 458, 666, 620, 363, 127, 191, 782, 407, 436, 626,
    571, 465, 681, 246, 707, 350, 599, 668, 790, 460, 249, 682, 573, 411, 803, 789, 709, 365, 440, 628, 689, 374, 423,
    466, 793, 250, 371, 481, 574, 413, 603, 366, 468, 655, 900, 805, 615, 684, 710, 429, 794, 252, 373, 605, 848, 690,
    713, 632, 482, 806, 427, 904, 414, 223, 663, 692, 835, 619, 472, 455, 796, 809, 714, 721, 837, 716, 864, 810, 606,
    912, 722, 696, 377, 435, 817, 319, 621, 812, 484, 430, 838, 667, 488, 239, 378, 459, 622, 627, 437, 380, 818, 461,
    496, 669, 679, 724, 841, 629, 351, 467, 438, 737, 251, 462, 442, 441, 469, 247, 683, 842, 738, 899, 670, 783, 849,
    820, 728, 928, 791, 367, 901, 630, 685, 844, 633, 711, 253, 691, 824, 902, 686, 740, 850, 375, 444, 470, 483, 415,
    485, 905, 795, 473, 634, 744, 852, 960, 865, 693, 797, 906, 715, 807, 474, 636, 694, 254, 717, 575, 913, 798, 811,
    379, 697, 431, 607, 489, 866, 723, 486, 908, 718, 813, 476, 856, 839, 725, 698, 914, 752, 868, 819, 814, 439, 929,
    490, 623, 671, 739, 916, 463, 843, 381, 497, 930, 821, 726, 961, 872, 492, 631, 729, 700, 443, 741, 845, 920, 382,
    822, 851, 730, 498, 880, 742, 445, 471, 635, 932, 687, 903, 825, 500, 846, 745, 826, 732, 446, 962, 936, 475, 853,
    867, 637, 907, 487, 695, 746, 828, 753, 854, 857, 504, 799, 255, 964, 909, 719, 477, 915, 638, 748, 944, 869, 491,
    699, 754, 858, 478, 968, 383, 910, 815, 976, 870, 917, 727, 493, 873, 701, 931, 756, 860, 499, 731, 823, 922, 874,
    918, 502, 933, 743, 760, 881, 494, 702, 921, 501, 876, 847, 992, 447, 733, 827, 934, 882, 937, 963, 747, 505, 855,
    924, 734, 829, 965, 938, 884, 506, 749, 945, 966, 755, 859, 940, 830, 911, 871, 639, 888, 479, 946, 750, 969, 508,
    861, 757, 970, 919, 875, 862, 758, 948, 977, 923, 972, 761, 877, 952, 495, 703, 935, 978, 883, 762, 503, 925, 878,
    735, 993, 885, 939, 994, 980, 926, 764, 941, 967, 886, 831, 947, 507, 889, 984, 751, 942, 996, 971, 890, 509, 949,
    973, 1000, 892, 950, 863, 759, 1008, 510, 979, 953, 763, 974, 954, 879, 981, 982, 927, 995, 765, 956, 887, 985,
    997, 986, 943, 891, 998, 766, 511, 988, 1001, 951, 1002, 893, 975, 894, 1009, 955, 1004, 1010, 957, 983, 958, 987,
    1012, 999, 1016, 767, 989, 1003, 990, 1005, 959, 1011, 1013, 895, 1006, 1014, 1017, 1018, 991, 1020, 1007, 1015,
    1019, 1021, 1022, 1023], "int")
# fmt: on

# modified from sionna
# https://github.com/NVlabs/sionna/blob/main/sionna/fec/polar/utils.py
def generate_5g_ranking(k, n, sort=True):
    """Returns information and frozen bit positions of the 5G Polar code
    as defined in Tab. 5.3.1.2-1 in [3GPPTS38212]_ for given values of ``k``
    and ``n``.
    Input
    -----
        k: int
            The number of information bit per codeword.
        n: int
            The desired codeword length. Must be a power of two.
        sort: bool
            Defaults to True. Indicates if the returned indices are
            sorted.
    Output
    ------
        [frozen_pos, info_pos]:
            List:
        frozen_pos: ndarray
            An array of ints of shape `[n-k]` containing the frozen
            position indices.
        info_pos: ndarray
            An array of ints of shape `[k]` containing the information
            position indices.
    Raises
    ------
        AssertionError
            If ``k`` or ``n`` are not positve ints.
        AssertionError
            If ``sort`` is not bool.
        AssertionError
            If ``k`` or ``n`` are larger than 1024
        AssertionError
            If ``n`` is less than 32.
        AssertionError
            If the resulting coderate is invalid (`>1.0`).
        AssertionError
            If ``n`` is not a power of 2.
    """
    # assert error if r>1 or k,n are negativ
    assert isinstance(k, int), "k must be integer."
    assert isinstance(n, int), "n must be integer."
    assert isinstance(sort, bool), "sort must be bool."
    assert k > -1, "k cannot be negative."
    assert k < 1025, "k cannot be larger than 1024."
    assert n < 1025, "n cannot be larger than 1024."
    assert n > 31, "n must be >=32."
    assert n >= k, "Invalid coderate (>1)."
    assert np.log2(n) == int(np.log2(n)), "n must be a power of 2."

    ind = np.argsort(frozen_pos_table)
    ch_order_sort = np.vstack((np.arange(1024)[ind], frozen_pos_table[ind])).astype("int")
    ch_order_sort_n = ch_order_sort[:, 0:n]  # only consider the first n channels
    ind_n = np.argsort(ch_order_sort_n[0, :])  # and sort again according to reliability
    ch_order_n = ch_order_sort_n[1, ind_n]

    frozen_pos = np.zeros(n - k, "int")
    info_pos = np.zeros(k, "int")
    # the n-k smallest positions of ch_order denote frozen pos.
    for i in range(n - k):
        frozen_pos[i] = ch_order_n[i]
    for i in range(n - k, n):
        info_pos[i - (n - k)] = ch_order_n[i]

    # sort to have channels in ascending order
    if sort:
        info_pos = np.sort(info_pos)
        frozen_pos = np.sort(frozen_pos)

    return [frozen_pos, info_pos]


def interleave(K):
    # 38.212 Table 5.3.1.1-1
    # fmt: off
    p_IL_max_table = [0, 2, 4, 7, 9, 14, 19, 20, 24, 25, 26, 28, 31, 34, 42, 45, 49, 50, 51, 53, 54, 56, 58, 59, 61,
                      62, 65, 66, 67, 69, 70, 71, 72, 76, 77, 81, 82, 83, 87, 88, 89, 91, 93,95, 98, 101, 104, 106,
                      108, 110, 111, 113, 115, 118, 119, 120, 122, 123, 126, 127, 129, 132, 134, 138, 139, 140, 1, 3,
                      5, 8, 10, 15, 21, 27, 29, 32, 35, 43, 46, 52, 55, 57, 60, 63, 68, 73, 78, 84, 90, 92, 94, 96,
                      99, 102, 105, 107, 109, 112, 114, 116, 121, 124, 128, 130, 133, 135, 141, 6, 11, 16, 22, 30, 33,
                      36, 44, 47, 64, 74, 79, 85, 97, 100, 103, 117, 125, 131, 136, 142, 12, 17, 23, 37, 48, 75, 80,
                      86, 137, 143, 13, 18, 38, 144, 39, 145, 40, 146, 41, 147, 148, 149, 150, 151, 152, 153, 154, 155,
                      156, 157, 158, 159, 160, 161, 162, 163]
    # fmt: on
    k = 0
    K_IL_max = 164
    p = np.empty(K, "int")
    for p_IL_max in p_IL_max_table:
        if p_IL_max >= (K_IL_max - K):
            p[k] = p_IL_max - (K_IL_max - K)
            k += 1
    return p


# very simple successive cancellation decoder
def Polar_SC_decoder(N, frozen_pos, r):
    n = np.log2(N).astype("int")
    L = np.zeros((n + 1, N))
    ucap = np.zeros((n + 1, N))
    ns = np.zeros(2 * N - 1, "int")
    L[0, :] = r
    node = depth = done = 0
    while done == 0:
        if depth == n:
            ucap[n, node] = 0 if (L[n, node] >= 0 or node in frozen_pos) else 1
            if node == N - 1:
                done = 1
            else:
                node = node // 2  # go to parent
                depth -= 1
        else:
            npos = int(2**depth - 1 + node)
            temp = 2 ** (n - depth)
            ctemp = temp // 2
            Ln = L[depth, temp * node : temp * (node + 1)]  # incoming beliefs
            a = Ln[: temp // 2]
            b = Ln[temp // 2 :]
            lnode = 2 * node  # left node
            rnode = 2 * node + 1  # right node
            if ns[npos] == 0:
                node = lnode  # go to left node
                depth += 1
                L[depth, ctemp * node : ctemp * (node + 1)] = (
                    (1 - 2 * (a > 0)) * (1 - 2 * (b > 0)) * np.max((np.abs(a), np.abs(b)))
                )
            elif ns[npos] == 1:
                ucapn = ucap[depth + 1, ctemp * lnode : ctemp * (lnode + 1)]  # incoming decisions from left child
                node = rnode  # go to right node
                depth += 1
                L[depth, ctemp * node : ctemp * (node + 1)] = b + (1 - 2 * ucapn) * a
            else:
                ucapl = ucap[depth + 1, ctemp * lnode : ctemp * (lnode + 1)]
                ucapr = ucap[depth + 1, ctemp * rnode : ctemp * (rnode + 1)]
                ucap[depth, temp * node : temp * (node + 1)] = np.append(np.mod(ucapl + ucapr, 2), ucapr)  # combine
                node = node // 2  # go to parent node
                depth -= 1
            ns[npos] += 1
    return ucap.astype("int")[n, :]


# rec: Rate-recovered input, LLRs, length must be power of two
# K: length of information block in bits, includes CRC
# E: rate-matched output length in bits
# L: length of decoding list
# CRClen: number of appended CRC bits
def nrPolarDecode(rec, K, E, L, padCRC=False, nmax=9, iil=True, CRClen=24):
    if CRClen not in (6, 11, 24):
        print("Error: invalid CRClen value!")
        exit()
    if nmax not in (9, 10):
        print("Error: invalid nmax value!")
        exit()
    # TODO: what to do with E argument, it is currently deducted from rec shape
    N = 512
    frozen_pos, info_pos = generate_5g_ranking(K, N)

    decoded = Polar_SC_decoder(N, frozen_pos, rec)[info_pos]

    if iil:
        # deinterleave
        p_IL = interleave(K)
        decoded2 = np.empty(decoded.shape, "int")
        np.put(decoded2, p_IL, decoded)
    else:
        decoded2 = decoded

    return decoded2
