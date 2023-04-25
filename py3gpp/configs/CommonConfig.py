
class CommonConfig():
    def __init__(self):
        self._MappingType = "A"
        self._SymbolAllocation = [0, 14]
        self._PRBSet = list(range(0, 52))
        self._RNTI = 1
        self._EnablePTRS = 0

    @property
    def MappingType(self):
        return self._MappingType

    @MappingType.setter
    def MappingType(self, map_type):
        assert map_type in ["A", "B"], "The value must be in A or B"
        self._MappingType = map_type

    @property
    def SymbolAllocation(self):
        return self._SymbolAllocation

    @SymbolAllocation.setter
    def SymbolAllocation(self, sym_list):
        # assert prbset > 0 and prbset < self._n_size_bwp, "The value must be 0..n_size_bwp"
        self._SymbolAllocation = sym_list

    @property
    def PRBSet(self):
        return self._PRBSet

    @PRBSet.setter
    def PRBSet(self, prbset):
        assert min(prbset) >= 0 and max(prbset) <= 274, "The value must be 0..274"
        self._PRBSet = prbset

    @property
    def RNTI(self):
        return self._RNTI

    @RNTI.setter
    def RNTI(self, rnti):
        assert rnti >= 0 and rnti <= 65535, "The value must be 0..65535"
        self._RNTI = rnti

    @property
    def EnablePTRS(self):
        return self._EnablePTRS

    @EnablePTRS.setter
    def EnablePTRS(self, enable):
        assert enable in [0, 1], "The value must be 0 or 1"
        self._EnablePTRS = enable