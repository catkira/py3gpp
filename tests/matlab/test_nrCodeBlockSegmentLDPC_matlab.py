import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrCodeBlockSegmentLDPC import nrCodeBlockSegmentLDPC
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import test_data.ldpc

def run_nrCodeBlockSegmentLDPC_fixed_data(eng):
    bgn = 2
    blk = test_data.ldpc.decBits
    ref_cbs = eng.nrCodeBlockSegmentLDPC(eng.transpose(eng.double(blk)), eng.double(bgn))
    ref_cbs = np.asarray(ref_cbs)

    out_cbs = nrCodeBlockSegmentLDPC(blk, bgn)
    assert np.array_equal(ref_cbs, out_cbs)

def run_nrCodeBlockSegmentLDPC(blklen, eng):
    bgn = 2
    in_blk = np.random.randint(2, size = (blklen, 1))  # this is a transport block
    ref_cbs = eng.nrCodeBlockSegmentLDPC(eng.double(in_blk), eng.double(bgn))  # outputs code block segments
    ref_cbs = np.asarray(ref_cbs)

    out_cbs = nrCodeBlockSegmentLDPC(in_blk, bgn)
    assert np.array_equal(ref_cbs, out_cbs)

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

def test_nrCodeBlockSegmentLDPC_fixed_data(eng):
    run_nrCodeBlockSegmentLDPC_fixed_data(eng)

@pytest.mark.parametrize('blklen', [100, 1000, 4000, 4001, 10000])
def test_nrCodeBlockSegmentLDPC_matlab(blklen, eng):
    run_nrCodeBlockSegmentLDPC(blklen, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    run_nrCodeBlockSegmentLDPC(100, _eng)
    # run_nrCodeBlockSegmentLDPC_fixed_data(_eng)
    _eng.quit()