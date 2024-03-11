import numpy as np
import pytest
from py3gpp.nrPolarDecode import nrPolarDecode

def test_nrPolarDecode():
    nmax = 9
    K = 100

    # --- TESTCASE1 ---
    payload = np.ones(K).astype(int)
    cw = np.array([0,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    cw_llr = -2*cw.astype(np.float64) + 1
    cw_llr[100:300] = 0  # introduce some errors

    payload_decoded = nrPolarDecode(cw_llr, K, 512, 10, nmax = nmax, iil = False)
    assert payload_decoded.shape[0] == K
    assert np.array_equal(payload, payload_decoded)

    # --- TESTCASE2 ---
    payload = np.array([1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,1,1,0,1,0,1,0,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0,0,1,1,1,1,0,1,1,0,1,0,0,1,0,1,1])
    cw = np.array([0,0,1,1,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,1,0,1,0,0,0,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,1,0,1,0,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,0,0,0,0,1,1,1,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1,1,0,1])
    cw_llr = -2*cw.astype(np.float64) + 1
    cw_llr[100:300] = 0  # introduce some errors

    payload_decoded = nrPolarDecode(cw_llr, K, 512, 10, nmax = nmax, iil = False)
    assert payload_decoded.shape[0] == K
    assert np.array_equal(payload_decoded, payload)


if __name__ == '__main__':
    test_nrPolarDecode()