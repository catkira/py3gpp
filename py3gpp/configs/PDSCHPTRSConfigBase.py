
class PDSCHPTRSConfigBase():
    def __init__(self):
        self._TimeDensity = 1
        self._FrequencyDensity = 2
        self._REOffset = '00'

    @property
    def TimeDensity(self):
        return self._TimeDensity

    @TimeDensity.setter
    def TimeDensity(self, td):
        assert td in [1, 2, 4], "The value must be 1, 2 or 4"
        self._TimeDensity = td

    @property
    def FrequencyDensity(self):
        return self._FrequencyDensity

    @FrequencyDensity.setter
    def FrequencyDensity(self, fd):
        assert fd in [2, 4], "The value must be 2 or 4"
        self._FrequencyDensity = fd

    @property
    def REOffset(self):
        return self._REOffset

    @REOffset.setter
    def REOffset(self, offset):
        assert offset in ['00', '01', '10', '11'], "The value must be in ['00', '01', '10', '11']"
        self._REOffset = offset
