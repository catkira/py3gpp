from py3gpp.nrPDSCHDMRSConfig import nrPDSCHDMRSConfig

class nrPDSCHDMRSConfig():
     def __init__(self):
          self._n_rb_size = 12
          self._nSizeBWP = 0
          self._nStartBWP = 0
          self._MappingType = "A"

          self._dmrs_typeA_pos = 2
          self._dmrs_len = 1
          self._dmrs_additional_pos = 1
          self._dmrs_conf_type = 2
          self._dmrs_port_set = 0
          self._num_CDM_groups_without_data = 1
          self._dmrs_NIDNSCID = 1
          self._dmrs_NSCID = 0
          self._PRB_set = list(range(0, self._n_size_bwp))
          self._symbol_allocation = [2, 12]

     @property
     def n_rb_size(self):
         return self._n_rb_size

     @property
     def nSizeBWP(self):
         return self._nSizeBWP

     @nSizeBWP.setter
     def nSizeBWP(self, size):
         assert size > 1 and size < 275, "The value must be in the range 1...275."
         self._nSizeBWP = size

     @property
     def nStartBWP(self):
         return self._nStartBWP

     @nStartBWP.setter
     def nStartBWP(self, start):
         assert start >= 0 and start < 2473, "The value must be in the range 0...2473."
         self._nStartBWP = start

     @property
     def MappingType(self):
         return self._MappingType

     @MappingType.setter
     def MappingType(self, map_type):
         assert map_type in ["A", "B"], "The value must be in A or B"
         self._MappingType = map_type

     @property
     def dmrs_typeA_pos(self):
         return self._dmrs_typeA_pos

     @dmrs_typeA_pos.setter
     def dmrs_typeA_pos(self, pos):
         assert pos in [2, 3], "The value must be 2 or 3"
         self._dmrs_typeA_pos = pos

     @property
     def dmrs_len(self):
         return self._dmrs_len

     @dmrs_len.setter
     def dmrs_len(self, length):
         assert length in [1, 2], "The value must be 1 or 2"
         self._dmrs_len = length

     @property
     def dmrs_additional_pos(self):
         return self._dmrs_additional_pos

     @dmrs_additional_pos.setter
     def dmrs_additional_pos(self, pos):
         assert pos in list(range(0,4)), "The value must be 0..3"
         self._dmrs_additional_pos = pos

     @property
     def dmrs_conf_type(self):
         return self._dmrs_conf_type

     @dmrs_conf_type.setter
     def dmrs_conf_type(self, conf_type):
         assert conf_type in [1, 2], "The value must be 1 or 2"
         self._dmrs_conf_type = conf_type

     @property
     def dmrs_port_set(self):
         assert False, "Not implemented!"
         return self._dmrs_port_set

     @dmrs_port_set.setter
     def dmrs_port_set(self, port_set):
         assert False, "Not implemented!"
         assert port_set in list(range(0, 11)), "The value must be 0..1"
         self._dmrs_port_set = port_set

     @property
     def num_CDM_groups_without_data(self):
         assert False, "Not implemented!"
         return self._num_CDM_groups_without_data

     @num_CDM_groups_without_data.setter
     def num_CDM_groups_without_data(self, num):
         assert False, "Not implemented!"
         assert num in list(range(0, 11)), "The value must be 0..1"
         self._num_CDM_groups_without_data = num

     @property
     def dmrs_NIDNSCID(self):
         return self._dmrs_NIDNSCID

     @dmrs_NIDNSCID.setter
     def dmrs_NIDNSCID(self, nid):
         assert nid > 0 and nid < 65535, "The value must be 0..65535"
         self._dmrs_NIDNSCID = nid

     @property
     def dmrs_NSCID(self):
         return self._dmrs_NIDNSCID

     @dmrs_NSCID.setter
     def dmrs_NSCID(self, nscid):
         assert nscid in [0, 1], "The value must be 0 or 1"
         self._dmrs_NSCID = nscid

     @property
     def PRB_set(self):
         return self._PRB_set

     @PRB_set.setter
     def PRB_set(self, prbset):
         assert min(prbset) >= 0 and max(prbset) < self._n_size_bwp, "The value must be 0..n_size_bwp"
         self._PRB_set = prbset

     @property
     def symbol_allocation(self):
         return self._symbol_allocation

     @symbol_allocation.setter
     def symbol_allocation(self, sym_list):
         # assert prbset > 0 and prbset < self._n_size_bwp, "The value must be 0..n_size_bwp"
         self._symbol_allocation = sym_list