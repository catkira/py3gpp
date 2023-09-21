import numpy as np
from py3gpp.nrLayerMap import nrLayerMap


def test_nrLayerMap_one_codeword_array():

    # Test for one codeword (array)
    in_symbols = np.ones((40, 1))
    nLayers = 4
    out = nrLayerMap(in_symbols, nLayers)
    # Replace with the expected result for your specific inputs
    expected_result = np.array([[10.0, 4.0]])
    assert np.array_equal(out, expected_result), f"Expected: {expected_result}, Actual: {out}"


def test_nrLayerMap_one_codeword_array_list():

    # Test for one codeword (array in a list)
    in_symbols = [np.ones((40, 1))]
    nLayers = 4
    out = nrLayerMap(in_symbols, nLayers)
    # Replace with the expected result for your specific inputs
    expected_result = np.array([[10.0, 4.0]])
    assert np.array_equal(out, expected_result), f"Expected: {expected_result}, Actual: {out}"


def test_nrLayerMap_two_codeword_array_list():

    # Test for two codeword (array in a list)
    in_symbols = [np.ones((20, 1)), np.ones((30, 1))]
    nLayers = 5
    out = nrLayerMap(in_symbols, nLayers)
    # Replace with the expected result for your specific inputs
    expected_result = np.array([[10.0, 5.0]])
    assert np.array_equal(out, expected_result), f"Expected: {expected_result}, Actual: {out}"


if __name__ == '__main__':
    test_nrLayerMap_one_codeword_array()
    test_nrLayerMap_one_codeword_array_list()
    test_nrLayerMap_two_codeword_array_list()
