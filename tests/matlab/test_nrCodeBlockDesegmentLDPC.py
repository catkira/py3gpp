import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrCodeBlockDesegmentLDPC import nrCodeBlockDesegmentLDPC
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import test_data.ldpc

def run_nrCodeBlockDesegmentLDPC_fixed_data(eng):
    bgn = 2
    blklen = 640 + 16 # 16 bit transport block CRC
    cbs = test_data.ldpc.decBits
    cbs = np.expand_dims(cbs, axis=1)
    ref_data = eng.nrCodeBlockDesegmentLDPC(eng.transpose(eng.double(test_data.ldpc.decBits)), eng.double(bgn), eng.double(blklen))
    ref_data = np.asarray(ref_data)

    data, _ = nrCodeBlockDesegmentLDPC(cbs, bgn, blklen)
    assert (ref_data == data).all()

def run_nrCodeBlockDesegmentLDPC(blklen, eng):
    bgn = 2
    in_blk = np.random.randint(2, size = (blklen, 1))  # this is a transport block
    cbs = eng.nrCodeBlockSegmentLDPC(eng.double(in_blk), eng.double(bgn))  # outputs code block segments
    cbs = np.asarray(cbs)
    ref_blk = eng.nrCodeBlockDesegmentLDPC(eng.double(cbs), eng.double(bgn), eng.double(blklen))
    ref_blk = np.asarray(ref_blk).astype(int)
    assert np.array_equal(ref_blk, in_blk)

    out_blk, _ = nrCodeBlockDesegmentLDPC(cbs, bgn, blklen)
    assert np.array_equal(ref_blk, out_blk)

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

def test_nrCodeBlockDesegmentLDPC_fixed_data(eng):
    run_nrCodeBlockDesegmentLDPC_fixed_data(eng)

@pytest.mark.parametrize('blklen', [100, 1000, 4000, 4001, 10000])
def test_nrCodeBlockDesegmentLDPC(blklen, eng):
    run_nrCodeBlockDesegmentLDPC(blklen, eng)

if __name__ == '__main__':
    _eng = matlab.engine.connect_matlab()
    run_nrCodeBlockDesegmentLDPC(4000, _eng)
    # run_nrCodeBlockDesegmentLDPC_fixed_data(_eng)
    _eng.quit()