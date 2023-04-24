import matlab.engine
import numpy as np
import pytest
import itertools

from py3gpp.nrSymbolModulate import nrSymbolModulate

def get_bin_symbols(bps, symbols):
    databits = np.array(list(range(symbols)))
    databits = np.array([(x & (2**np.arange(bps)) != 0).astype(int) for x in databits])
    return np.concatenate(databits, axis=0)

def run_nr_mapper(eng, modtype):
    if modtype == 'bpsk':
        databits = get_bin_symbols(1, 2)
        ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), "BPSK")
        data = nrSymbolModulate(databits, modtype)

    elif modtype == 'bpsk_pi2':
        databits = get_bin_symbols(1, 2)
        ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), "pi/2-BPSK")
        data = nrSymbolModulate(databits, modtype)

    elif modtype == 'qpsk':
        databits = get_bin_symbols(2, 4)
        ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), "QPSK")
        data = nrSymbolModulate(databits, modtype)

    elif modtype == 'qam16':
        databits = get_bin_symbols(4, 16)
        ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), "16QAM")
        data = nrSymbolModulate(databits, modtype)

    elif modtype == 'qam64':
        databits = get_bin_symbols(6, 64)
        ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), "64QAM")
        data = nrSymbolModulate(databits, modtype)

    elif modtype == 'qam256':
        databits = get_bin_symbols(8, 256)
        ref_data = eng.nrSymbolModulate(eng.transpose(eng.logical(databits)), "256QAM")
        data = nrSymbolModulate(databits, modtype)

    ref_data = np.around(np.array(list(itertools.chain(*ref_data))), 4)
    data = np.around(data, 4)

    assert (ref_data == data).all()

@pytest.mark.parametrize("modtype", ['bpsk', 'bpsk_pi2', 'qpsk', 'qam16', 'qam64', 'qam256'])
def test_nr_pbch(modtype):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_mapper(eng, modtype)
    finally:
        eng.quit()
