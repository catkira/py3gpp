
class nrNumerologyConfig:
        def __init__(self):
            self._subcarrier_spacing = 15
            self._cyclic_prefix = "normal"

        @property
        def subcarrier_spacing(self):
            return self._subcarrier_spacing

        @subcarrier_spacing.setter
        def subcarrier_spacing(self, spacing):
            assert spacing in [15, 30, 60, 120, 240], "The value must be [15, 30, 60, 120, 240]"
            self._subcarrier_spacing = spacing

        @property
        def cyclic_prefix(self):
            return self._cyclic_prefix

        @cyclic_prefix.setter
        def cyclic_prefix(self, pref):
            assert pref in ["normal", "extended"], "The value must be [15, 30, 60, 120, 240]"
            self._cyclic_prefix = pref