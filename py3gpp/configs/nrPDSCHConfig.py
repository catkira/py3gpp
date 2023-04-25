from .PDSCHConfigBase import PDSCHConfigBase
from .CommonConfig import CommonConfig

class nrPDSCHConfig(PDSCHConfigBase, CommonConfig):
    def __init__(self):
        super().__init__()
        self._Nid = 0
        self._NSizeBWP = []
        self._NStartBWP = []

    @property
    def NRBSize(self):
        return 12

    @property
    def Nid(self):
        return self._Nid

    @Nid.setter
    def Nid(self, nid):
        assert nid >= 0 and nid <= 1007, "The value must be in the range 0..1007."
        self._Nid = nid

    @property
    def NSizeBWP(self):
        return self._NSizeBWP

    @NSizeBWP.setter
    def NSizeBWP(self, size):
        assert size > 1 and size < 275, "The value must be in the range 1...275."
        self._NSizeBWP = size

    @property
    def NStartBWP(self):
        return self._NStartBWP

    @NStartBWP.setter
    def NStartBWP(self, start):
        assert start >= 0 and start < 2473, "The value must be in the range 0...2473."
        self._NStartBWP = start
