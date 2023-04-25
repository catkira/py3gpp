from py3gpp.nrPDSCHDMRSConfig import nrPDSCHDMRSConfig
from py3gpp.nrPDSCHPTRSConfig import nrPDSCHPTRSConfig

class PDSCHConfigBase():
     def __init__(self):
          self._Modulation = 'qpsk'
          self._NumLayers = 1
          self._ReservedPRB = None
          self._VRBToPRBInterleaving = 0
          self._VRBBundleSize = 2

          self.DMRS = nrPDSCHDMRSConfig()
          self.PTRS = nrPDSCHPTRSConfig()

     @property
     def Modulation(self):
         return self._Modulation

     @Modulation.setter
     def Modulation(self, mod):
         assert mod in ['qpsk', 'qam16', 'qam64', 'qam256'], "The value must be in ['qpsk', 'qam16', 'qam64', 'qam256']"
         self._Modulation = mod

     @property
     def NumLayers(self):
         return self._NumLayers

     @NumLayers.setter
     def NumLayers(self, N):
         assert N in list(range(1, 9)), "The value must be 1..8"
         self._NumLayers = N

     @property
     def ReservedPRB(self):
        raise NotImplementedError('not ready yet')
        return self._ReservedPRB

     @ReservedPRB.setter
     def ReservedPRB(self, N):
        raise NotImplementedError('not ready yet')
        self._ReservedPRB = None

     @property
     def VRBToPRBInterleaving(self):
        raise NotImplementedError('not ready yet')
        return self._VRBToPRBInterleaving

     @VRBToPRBInterleaving.setter
     def VRBToPRBInterleaving(self, N):
        raise NotImplementedError('not ready yet')
        assert N in [0, 1], "The value must be 0 or 1"
        self._VRBToPRBInterleaving = 0

     @property
     def VRBBundleSize(self):
        raise NotImplementedError('not ready yet')
        return self._VRBBundleSize

     @VRBToPRBInterleaving.setter
     def VRBBundleSize(self, N):
        raise NotImplementedError('not ready yet')
        assert N in [2, 4], "The value must be 2 or 4"
        self._VRBBundleSize = 0
