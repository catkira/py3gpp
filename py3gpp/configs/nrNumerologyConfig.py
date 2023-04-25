
class nrNumerologyConfig:
        def __init__(self):
            self._SubcarrierSpacing = 15
            self._CyclicPrefix = "normal"

        @property
        def SubcarrierSpacing(self):
            return self._SubcarrierSpacing

        @SubcarrierSpacing.setter
        def SubcarrierSpacing(self, spacing):
            assert spacing in [15, 30, 60, 120, 240], "The value must be [15, 30, 60, 120, 240]"
            self._SubcarrierSpacing = spacing

        @property
        def CyclicPrefix(self):
            return self._CyclicPrefix

        @CyclicPrefix.setter
        def CyclicPrefix(self, pref):
            assert pref in ["normal", "extended"], "The value must be in ['extended' or 'normal'']"
            self._CyclicPrefix = pref