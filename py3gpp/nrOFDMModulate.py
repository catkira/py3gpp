import numpy as np

def nrOFDMModulate(carrier, grid, CyclicPrefix = 'normal'):
    info = dict()
    mu = carrier["SubcarrierSpacing"]//15
    info["Nfft"] = 1024 * carrier["SubcarrierSpacing"]//15
    info["SampleRate"] = 15360000 * carrier["SubcarrierSpacing"]//15
    info["CyclicPrefixLengths"] = np.empty(0, 'int')
    info["SymbolLengths"] = np.empty(0, 'int')
    nSlots = grid.shape[1]
    waveform = np.empty(0, 'complex')
    if CyclicPrefix == 'normal':
        N_cp1 = int(144 * 2**(-mu) + 16)
        N_cp2 = int(144 * 2**(-mu))
    else:
        N_cp1 = int(512 * 2**(-mu))
        N_cp2 = N_cp1
    for slot_num in range(nSlots):
        if slot_num == 0 or slot_num == 7* 2**(mu):
            N_cp = N_cp1
        else:
            N_cp = N_cp2
        symbol_len = info["Nfft"] + N_cp
        nFill = (info["Nfft"] - grid.shape[0])//2
        full_slot_grid = np.concatenate([np.zeros(nFill), grid[:,0], np.zeros(nFill)])
        symbol_waveform = np.fft.fftshift(np.fft.fft(full_slot_grid))
        symbol_waveform_cp = np.append(symbol_waveform[:N_cp], symbol_waveform)
        waveform = np.append(waveform, symbol_waveform_cp)
        info["CyclicPrefixLengths"] = np.append(info["CyclicPrefixLengths"], N_cp)
        info["SymbolLengths"] = np.append(info["SymbolLengths"], symbol_len)
    return [waveform, info]