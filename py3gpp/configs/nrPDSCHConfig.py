from py3gpp.PDSCHConfigBase import PDSCHConfigBase

class nrPDSCHConfig(PDSCHConfigBase):
     def __init__(self):
          self._Nid = 0
          self._NSizeBWP = []
          self._NStartBWP = []
          self._MappingType = "A"
          self._EnablePTRS = 0

          self._PRBSet = list(range(0, self._NSizeBWP))
          self._symbol_allocation = [2, 12]

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
         return self._nStartBWP

     @NStartBWP.setter
     def NStartBWP(self, start):
         assert start >= 0 and start < 2473, "The value must be in the range 0...2473."
         self._NStartBWP = start

     @property
     def MappingType(self):
         return self._MappingType

     @MappingType.setter
     def MappingType(self, map_type):
         assert map_type in ["A", "B"], "The value must be in A or B"
         self._MappingType = map_type

     @property
     def PRBSet(self):
         return self._PRBSet

     @PRBSet.setter
     def PRBSet(self, prbset):
         assert min(prbset) >= 0 and max(prbset) < self._n_size_bwp, "The value must be 0..n_size_bwp"
         self._PRBSet = prbset

     @property
     def EnablePTRS(self):
         return self._EnablePTRS

     @EnablePTRS.setter
     def EnablePTRS(self, enable):
         assert enable in [0, 1], "The value must be 0 or 1"
         self._EnablePTRS = enable

     @property
     def symbol_allocation(self):
         return self._symbol_allocation

     @symbol_allocation.setter
     def symbol_allocation(self, sym_list):
         # assert prbset > 0 and prbset < self._n_size_bwp, "The value must be 0..n_size_bwp"
         self._symbol_allocation = sym_list