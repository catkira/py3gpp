from py3gpp.nrNumerologyConfig import nrNumerologyConfig

class nrCarrierConfig(nrNumerologyConfig):
        def __init__(self):
            self._n_cell_id = 1
            self._n_size_grid = 52
            self._n_start_grid = 0
            self._n_slot = 0
            self._n_frame = 0

            self.__symbols_per_slot = 0;
            self.__slots_per_subframe = 0;
            self.__slots_per_frame = 0;

        @property
        def symbols_per_slot(self):
            if self.cyclic_prefix == "normal":
                return 14
            else:
                return 12

        @property
        def slots_per_subframe(self):
            return self.subcarrier_spacing//15

        @property
        def slots_per_frame(self):
            return int(10*(self.subcarrier_spacing/15))

        @property
        def n_cell_id(self):
            return self._n_cell_id

        @n_cell_id.setter
        def n_cell_id(self, nid):
            assert nid >= 0 and nid <= 1007, "The value must be in the range 0...1007."
            self._n_cell_id = nid

        @property
        def n_size_grid(self):
            return self._n_size_grid

        @n_size_grid.setter
        def n_size_grid(self, size):
            assert size > 0 and size <= 275, "The value must be in the range 1...275."
            self._n_size_grid = size

        @property
        def n_start_grid(self):
            return self._n_start_grid

        @n_start_grid.setter
        def n_start_grid(self, start):
            assert start >= 0 and start <= 2199, "The value must be in the range 0...2999."
            self._n_start_grid = start

        @property
        def n_slot(self):
            return self._n_slot

        @n_slot.setter
        def n_slot(self, num):
            assert num >= 0, "The value must be scalar, nonnegative."
            self._n_slot = num

        @property
        def n_frame(self):
            return self._n_frame

        @n_frame.setter
        def n_frame(self, num):
            assert num >= 0, "The value must be scalar, nonnegative."
            self._n_frame = num