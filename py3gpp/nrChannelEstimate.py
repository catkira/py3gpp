import numpy as np
import scipy
from py3gpp import nrSetResources

def nrChannelEstimate(rxGrid = None, refInd = None, refSym = None, refGrid = None, carrier = None):
    cp = 'normal' if carrier is None else 'extended'
    if refGrid is None:
        if (refInd is None) or (refSym is None):
            print("Error: refInd and refSym need to be given when refGrid is None!")
            return
        refGrid = np.zeros(rxGrid.shape, 'complex')
        nrSetResources(refInd, refGrid, refSym)
    else:
        pilot_idx = np.where(refGrid.ravel(order='F') != 0)
        refInd = pilot_idx[0]
        refSym = refGrid.ravel(order='F')[refInd] 

    rxSym = rxGrid.ravel(order='F')[refInd]         
    L = 14 if cp == 'normal' else 12
    K = rxGrid.shape[0] # number of subcarriers
    N = rxGrid.shape[1] # number of symbols
    H = np.zeros(refGrid.shape, 'complex')
    R,C = np.mgrid[:K,:N]
    normGrid = rxGrid/refGrid
    idx_nonzero = np.where(np.invert(np.isinf(normGrid.ravel(order='F'))))[0]
    normXYZ = np.column_stack((C.ravel(order='F')[idx_nonzero], R.ravel(order='F')[idx_nonzero], normGrid.ravel(order='F')[idx_nonzero]))
    
    if True:
        # this one works best!
        for col in range(N):
            idx = np.where(np.logical_and(refInd >= col*K, refInd < (col+1)*K))[0]
            if len(idx) > 0:
                sym_idx = refInd[idx] - col*K
                H[:,col] = np.interp(np.arange(K), sym_idx, rxSym[idx]/refSym[idx])

        # estimate noise variance
        mean = np.mean((np.abs(H[:,1]), np.abs(H[:,3])), axis=0)
        nVar = np.mean(np.abs(np.abs(H[:,1]) - mean))

    elif False:
        H = scipy.interpolate.griddata((normXYZ[:,0].real, normXYZ[:,1].real), 
            normXYZ[:,2], (C.ravel(order='F'), R.ravel(order='F'))).reshape(refGrid.shape, order='F')
    elif False:    
        # use RBFInterpolator because interp2d and griddata cannot extrapolate
        interpolator = scipy.interpolate.RBFInterpolator(np.array((normXYZ[:,0].real, normXYZ[:,1].real)).T, normXYZ[:,2])
        H = interpolator(np.vstack((C.ravel(order='F'), R.ravel(order='F'))).T).reshape(refGrid.shape, order='F')     
    return H, nVar