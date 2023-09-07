import numpy as np
from py3gpp.nrTBS import nrTBS


def test_nrTBS_one_codeword():

    # Test for one codeword
    modulation = '16QAM'
    nlayers = 4
    nPRB = 52
    NREPerPRB = 120
    tcr = 0.48
    xOh = 6
    tbScaling = 0.25
    tb_one_cw = nrTBS(modulation, nlayers, nPRB,
                      NREPerPRB, tcr, xOh, tbScaling)
    # Replace with the expected result for your specific inputs
    expected_result_one = 11272
    assert tb_one_cw == expected_result_one, f"Expected: {expected_result_one}, Actual: {tb_one_cw}"


def test_nrTBS_two_codewords():
    # Test for two codewords
    modulation = ['QPSK', '64QAM']
    nlayers = 8
    nPRB = 106
    NREPerPRB = 100
    tcr = [0.3701, 0.4277]
    xOh = 0
    tbScaling = 1
    tb_two_cw = nrTBS(modulation, nlayers, nPRB,
                      NREPerPRB, tcr, xOh, tbScaling)
    # Replace with the expected result for your specific inputs
    expected_result_two = np.array([31240, 108552])
    assert np.array_equal(
        tb_two_cw, expected_result_two), f"Expected: {expected_result_two}, Actual: {tb_two_cw}"


if __name__ == '__main__':
    test_nrTBS_one_codeword()
    test_nrTBS_two_codewords()
