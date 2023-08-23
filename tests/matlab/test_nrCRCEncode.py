import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrCRCEncode import nrCRCEncode

def run_nr_crc_encode(poly, blk_size, eng):
    blk_bits = eng.randi(matlab.double([0, 1]), blk_size, 1)

    ref_data = eng.nrCRCEncode(blk_bits, poly)
    ref_data = np.asarray(ref_data)

    blk_bits = np.asarray(blk_bits)
    data = nrCRCEncode(blk_bits, poly)

    assert np.all(ref_data == data)

@pytest.mark.parametrize("poly", ["6", "11", "16", "24A", "24B", "24C"])
@pytest.mark.parametrize("blk_size", [100, 2000])
def test_nr_crc_encode(poly, blk_size):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_crc_encode(poly, blk_size, eng)
    finally:
        eng.quit()

if __name__ == '__main__':
    test_nr_crc_encode("11", 2000)
