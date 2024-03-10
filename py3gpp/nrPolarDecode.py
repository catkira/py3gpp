import numpy as np
from py3gpp.helper import generate_5g_ranking
from py3gpp.helper import polar_precode_interleave

# very simple successive cancellation decoder
def Polar_SC_decoder(N, frozen_pos, r):
    n = np.log2(N).astype("int")
    L = np.zeros((n + 1, N))
    ucap = np.zeros((n + 1, N))
    ns = np.zeros(2 * N - 1, "int")  # node state vector
    L[0, :] = r
    node = depth = done = 0
    while done == 0:
        # print(f'd = {depth}, node = {node}')
        if depth == n:
            ucap[n, node] = 0 if ((L[n, node] >= 0) or (node in frozen_pos)) else 1
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
                    np.sign(a) * np.sign(b) * np.max((np.abs(a), np.abs(b)))  # minsum-function
                )
            elif ns[npos] == 1:
                ucapn = ucap[depth + 1, ctemp * lnode : ctemp * (lnode + 1)]  # incoming decisions from left child
                node = rnode  # go to right node
                depth += 1
                L[depth, ctemp * node : ctemp * (node + 1)] = b + (1 - 2 * ucapn) * a # g-function
            elif ns[npos] == 2:
                ucapl = ucap[depth + 1, ctemp * lnode : ctemp * (lnode + 1)]
                ucapr = ucap[depth + 1, ctemp * rnode : ctemp * (rnode + 1)]
                ucap[depth, temp * node : temp * (node + 1)] = np.append(np.mod(ucapl + ucapr, 2), ucapr)  # combine
                node = node // 2  # go to parent node
                depth -= 1
            else:
                assert False
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
        p_IL = polar_precode_interleave(K)
        decoded2 = np.empty(decoded.shape, "int")
        np.put(decoded2, p_IL, decoded)
    else:
        decoded2 = decoded

    return decoded2

if __name__ == '__main__':
    import py3gpp
    import sionna
    nmax = 9
    K = 100

    # --- TESTCASE1 ---
    payload = np.ones(K).astype(int)
    cw = py3gpp.nrPolarEncode(payload, 512, nmax=nmax, iil=False)
    cw_desired = np.array([0,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    assert np.array_equal(cw, cw_desired)
    
    cw_llr = -2*cw.astype(np.float64) + 1
    cw_llr[100:300] = 0  # introduce some errors

    frozen_pos, info_pos = sionna.fec.polar.utils.generate_5g_ranking(K, 2**nmax)
    decoder = sionna.fec.polar.decoding.PolarSCLDecoder(frozen_pos, 2**nmax, list_size=8, crc_degree='CRC24C', cpu_only=True, use_fast_scl=False)
    payload_decoded_sionna = np.array(decoder(np.expand_dims(-cw_llr, 0))[0], 'int')
    print(payload_decoded_sionna)
    assert np.array_equal(payload, payload_decoded_sionna)

    payload_decoded = py3gpp.nrPolarDecode(cw_llr, K, 512, 10, nmax = nmax, iil = False)
    assert payload_decoded.shape[0] == K
    print(payload_decoded)
    # assert np.array_equal(payload, payload_decoded)

    # --- TESTCASE2 ---
    payload = np.array([1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,1,1,0,1,0,1,0,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0,0,1,1,1,1,0,1,1,0,1,0,0,1,0,1,1])
    cw = np.array([0,0,1,1,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,1,0,1,0,0,0,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,1,0,1,0,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,0,0,0,0,1,1,1,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1,1,0,1])
    cw_llr = -2*cw.astype(np.float64) + 1
    cw_llr[100:300] = 0  # introduce some errors

    payload_decoded_sionna = np.array(decoder(np.expand_dims(-cw_llr, 0))[0], 'int')
    print(payload_decoded_sionna)
    assert np.array_equal(payload_decoded_sionna, payload)

    payload_decoded = py3gpp.nrPolarDecode(cw_llr, K, 512, 10, nmax = nmax, iil = False)
    assert payload_decoded.shape[0] == K
    print(payload_decoded)
    assert np.array_equal(payload_decoded, payload)
