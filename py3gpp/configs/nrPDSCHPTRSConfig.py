from py3gpp.PDSCHPTRSConfigBase import PDSCHPTRSConfigBase

class nrPDSCHPTRSConfig(PDSCHPTRSConfigBase):
    def __init__(self):
        self._PTRSPortSet = []

    @property
    def PTRSPortSet(self):
        raise NotImplementedError('not ready yet')
        return self._PTRSPortSet

    @PTRSPortSet.setter
    def PTRSPortSet(self, size):
        raise NotImplementedError('not ready yet')
        self._PTRSPortSet = size
