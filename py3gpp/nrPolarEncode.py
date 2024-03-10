import numpy as np
from py3gpp.helper import generate_5g_ranking

def nrPolarEncode(payload, E, nmax = 9 , iil = False):
    _, info_pos = generate_5g_ranking(k = payload.shape[0], n = 2 ** nmax)
    N = 2 ** nmax
    u = np.zeros(N).astype(int)
    u[info_pos] = payload.astype(int)
    G_N = int(1)
    for _ in range(nmax):
        G_N = np.kron(G_N, np.array([[1, 0], [1, 1]]).astype(int))
    cw = np.mod(np.matmul(u, G_N), 2)
    return cw


if __name__ == '__main__':
    import py3gpp
    nmax = 9
    payload = np.ones(100).astype(int)
    cw = py3gpp.nrPolarEncode(payload, 512, nmax=nmax)
    cw_desired = np.array([0,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    assert np.array_equal(cw, cw_desired)

    payload_decoded = py3gpp.nrPolarDecode(cw, payload.shape[0], 512, 10, nmax = nmax, iil = False)
    assert payload_decoded.shape[0] == payload.shape[0]
    print(payload_decoded)