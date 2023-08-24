import numpy as np
import scipy as sp
from importlib_resources import files, as_file # importlib.resources only works for Python >= 3.9
from py3gpp.nrDLSCHInfo import getZlist
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

def nrLDPCEncode(cbs, bgn):
    assert len(cbs.shape) == 2, 'cbs must be a 2-dimensional matrix'
    K = cbs.shape[0]  # length of a code segment
    C = cbs.shape[1]  # number of code segments
    
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
    codedcbs = np.zeros((N + 2 * Zc, C))

    # replace filler bits with 0
    fill_indices = (cbs[:, 0] == -1)  # filler bits are at identical locations in every segment
    cbs[fill_indices, :] = 0

    # encode
    bm = _load_basegraph(7, bgn)
    pcm = _lift_basegraph(bm, Zc)

    # set filler bits back to -1
    fill_indices_out = np.append(fill_indices, np.repeat(False, N + 2 * Zc - K))
    codedcbs[fill_indices_out, :] = -1

    # puncture first 2 * Zc systematic bits
    codedcbs = codedcbs[2 * Zc :, :]

    return codedcbs

if __name__ == '__main__':
    bgn = 2
    C = 2
    K = 2560
    F = 36
    cbs = np.ones((K - F, C))
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    codedcbs = nrLDPCEncode(cbs, bgn)
    print(codedcbs.shape)
