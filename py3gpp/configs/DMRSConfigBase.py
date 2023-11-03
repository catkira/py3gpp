
class DMRSConfigBase():
     def __init__(self):
        self._NLayers = 1
        self._Ports = None
        self._DMRSTypeAPosition = 2
        self._DMRSAdditionalPosition = 0
        self._DMRSLength = 1
        self._CustomSymbolSet = []
        self._DMRSPortSet = []
        self._NIDNSCID = []
        self._NSCID = 0

     @property
     def NLayers(self):
        return self._NLayers

     @NLayers.setter
     def NLayers(self, N):
        assert N > 0
        self._NLayers = N

     @property
     def Ports(self):
        return self._Ports

     @property
     def DMRSTypeAPosition(self):
        return self._DMRSTypeAPosition

     @DMRSTypeAPosition.setter
     def DMRSTypeAPosition(self, pos):
        assert pos in [2, 3]
        self._DMRSTypeAPosition = pos

     @property
     def DMRSAdditionalPosition(self):
        return self._DMRSAdditionalPosition

     @DMRSAdditionalPosition.setter
     def DMRSAdditionalPosition(self, pos):
        assert pos in list(range(4))
        self._DMRSAdditionalPosition = pos

     @property
     def DMRSLength(self):
        return self._DMRSLength

     @DMRSLength.setter
     def DMRSLength(self, pos):
        assert pos in list(range(4))
        self._DMRSLength = pos

     @property
     def CustomSymbolSet(self):
        raise NotImplementedError('not ready yet')
        return self._CustomSymbolSet

     @CustomSymbolSet.setter
     def CustomSymbolSet(self, set):
        raise NotImplementedError('not ready yet')
        self._CustomSymbolSet = set

     @property
     def DMRSPortSet(self):
        raise NotImplementedError('not ready yet')
        return self._DMRSPortSet

     @DMRSPortSet.setter
     def DMRSPortSet(self, set):
        raise NotImplementedError('not ready yet')
        self._DMRSPortSet = set

     @property
     def NIDNSCID(self):
        return self._NIDNSCID

     @NIDNSCID.setter
     def NIDNSCID(self, nid):
        assert nid >= 0 and nid <= 65535, "The value must be 0..65535"
        self._NIDNSCID = nid

     @property
     def NSCID(self):
        return self._NSCID

     @NSCID.setter
     def NSCID(self, nscid):
        assert nscid in [0, 1], "The value must be 0 or 1"
        self._NSCID = nscid
