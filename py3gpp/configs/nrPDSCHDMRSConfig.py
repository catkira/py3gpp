from .DMRSConfigBase import DMRSConfigBase

class nrPDSCHDMRSConfig(DMRSConfigBase):
    def __init__(self):
        super().__init__()
        self._DMRSConfigurationType = 1
        self._DMRSReferencePoint = 'CRB0'
        self._NumCDMGroupsWithoutData = 2
        self._DMRSDownlinkR16 = 0

    @property
    def DMRSConfigurationType(self):
        return self._DMRSConfigurationType

    @DMRSConfigurationType.setter
    def DMRSConfigurationType(self, size):
        assert size in [1, 2], "The value must be 1 or 2."
        self._DMRSConfigurationType = size

    @property
    def DMRSReferencePoint(self):
        raise NotImplementedError('not ready yet')
        return self._DMRSReferencePoint

    @DMRSReferencePoint.setter
    def DMRSReferencePoint(self, size):
        raise NotImplementedError('not ready yet')
        assert size in ['CRB0', 'PRB0'], "The value must be 'CRB0' or 'PRB0'."
        self._DMRSReferencePoint = size

    @property
    def NumCDMGroupsWithoutData(self):
        raise NotImplementedError('not ready yet')
        return self._NumCDMGroupsWithoutData

    @NumCDMGroupsWithoutData.setter
    def NumCDMGroupsWithoutData(self, N):
        raise NotImplementedError('not ready yet')
        assert N in [1, 2, 3], "The value must be 1, 2 or 3."
        self._NumCDMGroupsWithoutData = N

    @property
    def DMRSDownlinkR16(self):
        raise NotImplementedError('not ready yet')
        return self._DMRSDownlinkR16

    @DMRSDownlinkR16.setter
    def DMRSDownlinkR16(self, N):
        raise NotImplementedError('not ready yet')
        self._DMRSDownlinkR16 = N
