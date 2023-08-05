from .nrNumerologyConfig import nrNumerologyConfig

class nrCarrierConfig(nrNumerologyConfig):
        def __init__(self, NCellID = 1, NSizeGrid = 52, NStartGrid = 0, NSlot = 0, NFrame = 0, SubcarrierSpacing = 15):
            super().__init__()
            self._NCellID = NCellID
            self._NSizeGrid = NSizeGrid
            self._NStartGrid = NStartGrid
            self._NSlot = NSlot
            self._NFrame = NFrame
            self.SubcarrierSpacing = SubcarrierSpacing

        @property
        def SymbolsPerSlot(self):
            if self.CyclicPrefix == "normal":
                return 14
            else:
                return 12

        @property
        def SlotsPerSubframe(self):
            return self.SubcarrierSpacing//15

        @property
        def SlotsPerFrame(self):
            return int(10*(self.SubcarrierSpacing/15))

        @property
        def NCellID(self):
            return self._NCellID

        @NCellID.setter
        def NCellID(self, nid):
            assert nid >= 0 and nid <= 1007, "The value must be in the range 0...1007."
            self._NCellID = nid

        @property
        def NSizeGrid(self):
            return self._NSizeGrid

        @NSizeGrid.setter
        def NSizeGrid(self, size):
            assert size > 0 and size <= 275, "The value must be in the range 1...275."
            self._NSizeGrid = size

        @property
        def NStartGrid(self):
            return self._NStartGrid

        @NStartGrid.setter
        def NStartGrid(self, start):
            assert start >= 0 and start <= 2199, "The value must be in the range 0...2999."
            self._NStartGrid = start

        @property
        def NSlot(self):
            return self._NSlot

        @NSlot.setter
        def NSlot(self, num):
            assert num >= 0, "The value must be scalar, nonnegative."
            self._NSlot = num

        @property
        def NFrame(self):
            return self._NFrame

        @NFrame.setter
        def NFrame(self, num):
            assert num >= 0, "The value must be scalar, nonnegative."
            self._NFrame = num