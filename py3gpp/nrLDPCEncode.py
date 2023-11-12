import numpy as np
import scipy as sp
from importlib_resources import files, as_file # importlib.resources only works for Python >= 3.9
from py3gpp.nrDLSCHInfo import getZlist, getZarray
from py3gpp import codes

# This function is from Sionna
def _load_basegraph(i_ls, bgn):
    if i_ls > 7:
        raise ValueError("i_ls too large.")

    if i_ls < 0:
        raise ValueError("i_ls cannot be negative.")

    # csv files are taken from 38.212 and dimension is explicitly given
    if bgn == 1:
        bm = np.zeros([46, 68]) - 1 # init matrix with -1 (None positions)
    elif bgn == 2:
        bm = np.zeros([42, 52]) - 1 # init matrix with -1 (None positions)
    else:
        raise ValueError("Basegraph not supported.")

    # and load the basegraph from csv format in folder "codes"
    source = source = files(codes).joinpath(f"bg{bgn}.csv")
    with as_file(source) as code:
        bg_csv = np.genfromtxt(code, delimiter=";")

    # reconstruct BG for given i_ls
    r_ind = 0
    for r in np.arange(2, bg_csv.shape[0]):
        # check for next row index
        if not np.isnan(bg_csv[r, 0]):
            r_ind = int(bg_csv[r, 0])
        c_ind = int(bg_csv[r, 1]) # second column in csv is column index
        value = bg_csv[r, i_ls + 2] # i_ls entries start at offset 2
        bm[r_ind, c_ind] = value

    return bm

# This function is from Sionna
def _lift_basegraph(bm, z):
    """Lift basegraph with lifting factor ``z`` and shifted identities as
    defined by the entries of ``bm``."""

    num_nonzero = np.sum(bm>=0) # num of non-neg elements in bm

    # init all non-zero row/column indices
    r_idx = np.zeros(z*num_nonzero)
    c_idx = np.zeros(z*num_nonzero)
    data = np.ones(z*num_nonzero)

    # row/column indices of identity matrix for lifting
    im = np.arange(z)

    idx = 0
    for r in range(bm.shape[0]):
        for c in range(bm.shape[1]):
            if bm[r,c]==-1: # -1 is used as all-zero matrix placeholder
                pass #do nothing (sparse)
            else:
                # roll matrix by bm[r,c]
                c_roll = np.mod(im+bm[r,c], z)
                # append rolled identity matrix to pcm
                r_idx[idx*z:(idx+1)*z] = r*z + im
                c_idx[idx*z:(idx+1)*z] = c*z + c_roll
                idx += 1

    # generate lifted sparse matrix from indices
    pcm = sp.sparse.csr_matrix((data,(r_idx, c_idx)),
                                shape=(z*bm.shape[0], z*bm.shape[1]))
    return pcm

# This function is from Sionna
def _gen_submat(bm, k_b, z, bgn):
    """Split the basegraph into multiple sub-matrices such that efficient
    encoding is possible.
    """
    g = 4 # code property (always fixed for 5G)
    mb = bm.shape[0] # number of CN rows in basegraph (BG property)

    bm_a = bm[0:g, 0:k_b]
    bm_b = bm[0:g, k_b:(k_b+g)]
    bm_c1 = bm[g:mb, 0:k_b]
    bm_c2 = bm[g:mb, k_b:(k_b+g)]

    # H could be sliced immediately (but easier to implement if based on B)
    hm_a = _lift_basegraph(bm_a, z)

    # not required for encoding, but helpful for debugging
    #hm_b = self._lift_basegraph(bm_b, z)

    hm_c1 = _lift_basegraph(bm_c1, z)
    hm_c2 = _lift_basegraph(bm_c2, z)

    hm_b_inv = _find_hm_b_inv(bm_b, z, bgn)

    return hm_a, hm_b_inv, hm_c1, hm_c2

# This function is from Sionna
def _find_hm_b_inv(bm_b, z, bgn):
    """ For encoding we need to find the inverse of `hm_b` such that
    `hm_b^-1 * hm_b = I`.

    Could be done sparse
    For BG1 the structure of hm_b is given as (for all values of i_ls)
    hm_b =
    [P_A I 0 0
        P_B I I 0
        0 0 I I
        P_A 0 0 I]
    where P_B and P_A are Shifted identities.

    The inverse can be found by solving a linear system of equations
    hm_b_inv =
    [P_B^-1, P_B^-1, P_B^-1, P_B^-1,
        I + P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1,
        P_A*P_B^-1, P_A*P_B^-1, I+P_A*P_B^-1, I+P_A*P_B^-1,
        P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1, I+P_A*P_B^-1].


    For bg2 the structure of hm_b is given as (for all values of i_ls)
    hm_b =
    [P_A I 0 0
        0 I I 0
        P_B 0 I I
        P_A 0 0 I]
    where P_B and P_A are Shifted identities

    The inverse can be found by solving a linear system of equations
    hm_b_inv =
    [P_B^-1, P_B^-1, P_B^-1, P_B^-1,
        I + P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1,
        I+P_A*P_B^-1, I+P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1,
        P_A*P_B^-1, P_A*P_B^-1, P_A*P_B^-1, I+P_A*P_B^-1]

    Note: the inverse of B is simply a shifted identity matrix with
    negative shift direction.
    """

    # permutation indices
    pm_a= int(bm_b[0,0])
    if bgn == 1:
        pm_b_inv = int(-bm_b[1, 0])
    else: # structure of B is slightly different for bg2
        pm_b_inv = int(-bm_b[2, 0])

    hm_b_inv = np.zeros([4*z, 4*z])

    im = np.eye(z)

    am = np.roll(im, pm_a, axis=1)
    b_inv = np.roll(im, pm_b_inv, axis=1)
    ab_inv = np.matmul(am, b_inv)

    # row 0
    hm_b_inv[0:z, 0:z] = b_inv
    hm_b_inv[0:z, z:2*z] = b_inv
    hm_b_inv[0:z, 2*z:3*z] = b_inv
    hm_b_inv[0:z, 3*z:4*z] = b_inv

    # row 1
    hm_b_inv[z:2*z, 0:z] = im + ab_inv
    hm_b_inv[z:2*z, z:2*z] = ab_inv
    hm_b_inv[z:2*z, 2*z:3*z] = ab_inv
    hm_b_inv[z:2*z, 3*z:4*z] = ab_inv

    # row 2
    if bgn == 1:
        hm_b_inv[2*z:3*z, 0:z] = ab_inv
        hm_b_inv[2*z:3*z, z:2*z] = ab_inv
        hm_b_inv[2*z:3*z, 2*z:3*z] = im + ab_inv
        hm_b_inv[2*z:3*z, 3*z:4*z] = im + ab_inv
    else: # for bg2 the structure is slightly different
        hm_b_inv[2*z:3*z, 0:z] = im + ab_inv
        hm_b_inv[2*z:3*z, z:2*z] = im + ab_inv
        hm_b_inv[2*z:3*z, 2*z:3*z] = ab_inv
        hm_b_inv[2*z:3*z, 3*z:4*z] = ab_inv

    # row 3
    hm_b_inv[3*z:4*z, 0:z] = ab_inv
    hm_b_inv[3*z:4*z, z:2*z] = ab_inv
    hm_b_inv[3*z:4*z, 2*z:3*z] = ab_inv
    hm_b_inv[3*z:4*z, 3*z:4*z] = im + ab_inv

    # return results as sparse matrix
    return sp.sparse.csr_matrix(hm_b_inv)

def _encode(s, pcm_a, pcm_b_inv, pcm_c1, pcm_c2):
    p_a = pcm_a * s
    p_a = pcm_b_inv * p_a

    p_b_1 = pcm_c1 * s.T
    p_b_2 = pcm_c2 * p_a.T
    p_b = p_b_1 + p_b_2

    c = np.concatenate((s, p_a, p_b)).astype(np.uint8)
    c = np.mod(c, 2)

    N = pcm_c1.shape[0] + pcm_a.shape[1] + pcm_b_inv.shape[0]
    assert c.shape[0] == N

    return c

def _mul_sh(x, k):
    if k == -1:
        return np.zeros(len(x))
    return np.roll(x, -int(k))


# this is like shown by Prof. Thangaraj in this video
# https://www.youtube.com/watch?v=QJwQi06Fm3M
# this is also how it would be done in hardware
def _encode_thangaraj(B, Zc, msg):
    M, N = B.shape
    cw = np.zeros(N * Zc)
    cw[:(N - M) * Zc] = msg # it's a systematic code

    temp = np.zeros(Zc, int)
    for i in range(4):
        for j in range(N - M):
            temp = np.mod(temp + _mul_sh(msg[j * Zc :][:Zc], B[i, j]), 2)
    
    p1_sh = B[1, N - M] if B[2, N - M] == -1 else B[2, N - M]
    cw[(N - M) * Zc :][: Zc] = _mul_sh(temp, Zc - p1_sh)

    # find p2, p3, p4
    for i in range(3):
        temp = np.zeros(Zc, int)
        for j in range(N - M + i + 1):
            temp = np.mod(temp + _mul_sh(cw[j * Zc :][:Zc], B[i, j]), 2)
        cw[(N - M + i + 1) * Zc :][: Zc] = temp

    # remaining parities
    for i in range(4, M):
        temp = np.zeros(Zc, int)
        for j in range(N - M + 4):
            temp = np.mod(temp + _mul_sh(cw[j * Zc :][:Zc], B[i, j]), 2)
        cw[(N - M + i) * Zc :][: Zc] = temp

    return cw


def nrLDPCEncode(cbs, bgn, algo = 'sionna'):
    cbs = cbs.copy() # don't modify inputs

    if algo not in ['sionna', 'thangaraj']:
        raise TypeError('algo has to be "sionna" or "thangaraj"')
    if len(cbs.shape) != 2:
        raise TypeError('cbs must be a 2-dimensional matrix')
    K = cbs.shape[0]  # length of a code segment
    C = cbs.shape[1]  # number of code segments
    if not (11 < K < 8449):
        raise ValueError('K must be 11 < K < 8449')

    # calculate Zc
    if bgn == 1:
        nsys = 22
        ncwnodes = 66
    else:
        nsys = 10
        ncwnodes = 50
    Zc = int(K / nsys)
    assert Zc in getZlist(), f'Zc = {Zc} is not a valid value'

    # calculate output size (N)
    N = int(Zc * ncwnodes)
    codedcbs = np.zeros((N + 2 * Zc, C)).astype(np.int8)

    # find i_ls
    if bgn == 1:
        k_b = 22
    elif bgn == 2:
        if K > 640:
            k_b = 10
        elif K > 560:
            k_b = 9
        elif K > 192:
            k_b = 8
        else:
            k_b = 6
    else:
        raise ValueError(f'bgn = {bgn} is not supported')

    Zarray = getZarray()
    min_val = 100000
    i_ls = None
    for i, s in enumerate(Zarray):
        for s1 in s:
            x = k_b * s1
            if  x >= K:
                # valid solution
                if x < min_val:
                    min_val = x
                    i_ls = i
    assert i is not None, 'could not find i_ls'
    # print(f'K = {K}, bgn = {bgn} => Zc = {Zc}, k_b = {k_b}, N = {N}, R = {K / N}, i_ls = {i_ls}')

    # replace filler bits with 0
    fill_indices = (cbs[:, 0] == -1)  # filler bits are at identical locations in every segment
    cbs[fill_indices, :] = 0 # set filler bits to 0

    # encode
    bm = _load_basegraph(i_ls, bgn)

    if algo == 'sionna':
        pcm = _lift_basegraph(bm, Zc)
        pcm_a, pcm_b_inv, pcm_c1, pcm_c2 = _gen_submat(bm, k_b, Zc, bgn)
        # print(f'pcm = {pcm.shape[0]} x {pcm.shape[1]} matrix')
        for i in range(cbs.shape[1]):
            codedcbs[:, i] = _encode(cbs[:, i], pcm_a, pcm_b_inv, pcm_c1, pcm_c2)

    elif algo == 'thangaraj':
        for i in range(cbs.shape[1]):
            codedcbs[:, i] = _encode_thangaraj(bm, Zc, cbs[:, i])

    # for i in range(cbs.shape[1]):
    #     if not _check_cw(bm, Zc, codedcbs[: , i]):
    #         print(f'Error: cw {i} is not valid')
    #     else:
    #         print(f'cw {i} is valid')

    # set filler bits back to -1
    fill_indices_out = np.append(fill_indices, np.repeat(False, N + 2 * Zc - K))
    codedcbs[fill_indices_out, :] = -1

    # puncture first 2 * Zc systematic bits
    codedcbs = codedcbs[2 * Zc :, :]

    return codedcbs

def _check_cw(B, Zc, cw):
    M, N = B.shape
    syn = np.zeros(M * Zc)
    for i in range(M):
        for j in range(N):
            syn[i * Zc :][: Zc] = np.mod(syn[i * Zc :][: Zc] + _mul_sh(cw[j * Zc :][: Zc], B[i, j]), 2)
    return not np.any(syn)

if __name__ == '__main__':
    bgn = 2
    C = 2
    K = 2560
    F = 36

    cbs = np.ones((K - F, C))
    cbs[0:10] = 0
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    codedcbs_1 = nrLDPCEncode(cbs.copy(), bgn, algo = 'sionna')
    
    codedcbs_2 = nrLDPCEncode(cbs, bgn, algo = 'thangaraj')
    
    assert codedcbs_1.shape == (12800, 2)
    assert codedcbs_2.shape == (12800, 2)
    assert np.array_equal(codedcbs_1, codedcbs_2)
