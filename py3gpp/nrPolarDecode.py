import numpy as np
from .helper import generate_5g_ranking

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
    N = 2**nmax
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
