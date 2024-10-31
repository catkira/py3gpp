import sys
import numpy as np
import pytest

from py3gpp.nrTransformPrecode import nrTransformPrecode
from py3gpp.nrTransformDeprecode import nrTransformDeprecode
from py3gpp.nrSymbolModulate import nrSymbolModulate

sys.path.append("test_data")

from test_data.transformPrecode import cw, desired_result_2, desired_result_40

def test_run_nrTransformPrecode_nrTransformDeprecode_2():
    modSym = nrSymbolModulate(cw, 'QPSK')
    result = nrTransformPrecode(modSym, 2)
    assert np.array_equal(np.round(result, 8), np.round(desired_result_2, 8))
    x = nrTransformDeprecode(result, 2)
    assert np.array_equal(np.round(x, 8), np.round(modSym, 8))

def test_run_nrTransformPrecode_nrTransformDeprecode_40():
    modSym = nrSymbolModulate(cw, 'QPSK')
    result = nrTransformPrecode(modSym, 40)
    assert np.array_equal(np.round(result, 8), np.round(desired_result_40, 8))
    x = nrTransformDeprecode(result, 40)
    assert np.array_equal(np.round(x, 8), np.round(modSym, 8))

if __name__ == '__main__':
    test_run_nrTransformPrecode_nrTransformDeprecode_2()
    test_run_nrTransformPrecode_nrTransformDeprecode_40()