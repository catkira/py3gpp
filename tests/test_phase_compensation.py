import numpy as np
import pytest

from py3gpp.nrOFDMModulate import nrOFDMModulate
from py3gpp.nrOFDMDemodulate import nrOFDMDemodulate
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

def test_phase_compensation():
    carrier = nrCarrierConfig(1, NSizeGrid = 30)
    Nfft = 512
    num_slots = 20
    expected_waveform_len = Nfft * num_slots + 36 * 17 + 40 * 3
    initial_N_slot_vector = [0, 4]
    f0_hz_vector = [0, 10e6, 11e6]
    for f0_hz in f0_hz_vector:
        for initial_N_slot in initial_N_slot_vector:
            print(f'testing f0 = {f0_hz} Hz, initialNSlot = {initial_N_slot}')
            test_symbol = np.ones((carrier.NSizeGrid * 12, 1), dtype = "complex")
            test_symbols = np.repeat(test_symbol, num_slots)
            test_symbols = np.reshape(test_symbols, (carrier.NSizeGrid * 12, num_slots))
            waveform, _ = nrOFDMModulate(carrier, test_symbols, CarrierFrequency = f0_hz, initialNSlot = initial_N_slot)
            assert waveform.shape[0] == expected_waveform_len
            rx_test_symbols = nrOFDMDemodulate(carrier, waveform, CarrierFrequency = f0_hz, initialNSlot = initial_N_slot)
            assert np.all(test_symbols == np.round(rx_test_symbols))
    
if __name__ == '__main__':
     test_phase_compensation()