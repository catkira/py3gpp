import matlab.engine
import numpy as np
import pytest
import itertools

from py3gpp.nrSymbolModulate import nrSymbolModulate

def get_bin_symbols(bps, symbols):
    databits = np.array(list(range(symbols)))
    databits = np.array([(x & (2**np.arange(bps)) != 0).astype(int) for x in databits])
    return np.concatenate(databits, axis=0)

def run_nr_mapper(databits, modtype, eng):
    ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), modtype)
    ref_data = np.around(np.array(list(itertools.chain(*ref_data))), 4)

    data = nrSymbolModulate(databits, modtype)
    data = np.around(data, 4)

    assert (ref_data == data).all()

@pytest.fixture(scope='session')
def eng():
    eng = matlab.engine.connect_matlab()
    yield eng
    eng.quit()

@pytest.mark.parametrize("modtype", ["BPSK", "pi/2-BPSK", "QPSK", "16QAM", "64QAM", "256QAM"])
def test_nr_pbch(modtype, eng):
    if modtype == "BPSK":
        databits = get_bin_symbols(1, 2)
    elif modtype == "pi/2-BPSK":
        databits = get_bin_symbols(1, 2)
    elif modtype == "QPSK":
        databits = get_bin_symbols(2, 4)
    elif modtype == "16QAM":
        databits = get_bin_symbols(4, 16)
    elif modtype == "64QAM":
        databits = get_bin_symbols(6, 64)
    elif modtype == "256QAM":
        databits = get_bin_symbols(8, 256)

    run_nr_mapper(databits, modtype, eng)
