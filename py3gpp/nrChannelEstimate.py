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
    L = 14 if cp == 'normal' else 12
    K = rxGrid.shape[0] # number of subcarriers
    N = rxGrid.shape[1] # number of symbols
    H = np.zeros(refGrid.shape, 'complex')
    R,C = np.mgrid[:K,:N]
    normGrid = rxGrid/refGrid
    idx_nonzero = np.where(np.invert(np.isinf(normGrid.ravel(order='F'))))[0]
    normXYZ = np.column_stack((C.ravel(order='F')[idx_nonzero], R.ravel(order='F')[idx_nonzero], normGrid.ravel(order='F')[idx_nonzero]))
    #interp_real = scipy.interpolate.interp2d(normXYZ[:,0].real, normXYZ[:,1].real, np.real(normXYZ[:,2]), kind='linear')
    #interp_imag = scipy.interpolate.interp2d(normXYZ[:,0].real, normXYZ[:,1].real, np.imag(normXYZ[:,2]), kind='linear')
    #H = interp_real(np.arange(K), np.arange(N)).reshape(refGrid.shape) + 1j*interp_imag(np.arange(K), np.arange(N)).reshape(refGrid.shape)
    
    # use RBFInterpolator because interp2d and griddata cannot extrapolate
    H = scipy.interpolate.griddata((normXYZ[:,0].real, normXYZ[:,1].real), 
        normXYZ[:,2], (C.ravel(order='F'), R.ravel(order='F'))).reshape(refGrid.shape, order='F')

    #H = scipy.interpolate.RBFInterpolator(np.array((normXYZ[:,0].real, normXYZ[:,1].real)).T, normXYZ[:,2])
    interpolator = scipy.interpolate.RBFInterpolator(np.array((normXYZ[:,0].real, normXYZ[:,1].real)).T, normXYZ[:,2])
    H = interpolator(np.vstack((C.ravel(order='F'), R.ravel(order='F'))).T).reshape(refGrid.shape, order='F')
    return H