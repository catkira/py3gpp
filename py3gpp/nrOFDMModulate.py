import numpy as np
from py3gpp import nrCarrierConfig
from py3gpp.nrOFDMInfo import nrOFDMInfo

# TODO: implement windowing
def nrOFDMModulate(carrier = None, grid = None, scs = None, initialNSlot = 0, CyclicPrefix = 'normal', Nfft = None, SampleRate = None, Windowing = None):
    info = dict()

    if carrier is None:
        if grid is None:
            print("Error: grid is needed when no carrierConfig is specified!")
            return
        NSizeGrid = grid.shape[0]//12            
        carrier = nrCarrierConfig(NSizeGrid = NSizeGrid)
    else:
        NSizeGrid = carrier.NSizeGrid          

    if scs == None:
            scs = carrier.SubcarrierSpacing        

    if Nfft == None:
        if SampleRate == None:
            Nfft = nrOFDMInfo(nrb = NSizeGrid, scs = scs)['Nfft']
            SampleRate = int(Nfft * scs * 1000)
        else:
            Nfft = int(SampleRate // scs // 1000)
    
    mu = (scs // 15) - 1

    info["Nfft"] = Nfft
    info["SampleRate"] = SampleRate
    info["CyclicPrefixLengths"] = np.empty(0, 'int')
    info["SymbolLengths"] = np.empty(0, 'int')
    if len(grid.shape) == 1:
        grid = grid[..., np.newaxis]
    nSlots = grid.shape[1]
    waveform = np.empty(0, 'complex')
    if CyclicPrefix == 'normal':
        N_cp1 = int(((144) * 2**(-mu) + 16) * (SampleRate/30720000))
        N_cp2 = int((144 * 2**(-mu)) * (SampleRate/30720000))
    else:
        N_cp1 = int((512 * 2**(-mu)) * (SampleRate/30720000))
        N_cp2 = N_cp1 

    for slot_num in range(nSlots):
        if slot_num == 0 or slot_num == 7 * 2**(mu):
            N_cp = N_cp1
        else:
            N_cp = N_cp2
        symbol_len = Nfft + N_cp
        nFill = (Nfft - grid.shape[0])//2
        if nFill < 0:
            full_slot_grid = grid[np.abs(nFill):, slot_num][:nFill]
        else:
            full_slot_grid = np.concatenate([np.zeros(nFill), grid[:,slot_num], np.zeros(nFill)])
        symbol_waveform = np.fft.ifft(np.fft.fftshift(full_slot_grid))
        symbol_waveform_cp = np.append(symbol_waveform[-N_cp:], symbol_waveform)
        waveform = np.append(waveform, symbol_waveform_cp)
        info["CyclicPrefixLengths"] = np.append(info["CyclicPrefixLengths"], N_cp)
        info["SymbolLengths"] = np.append(info["SymbolLengths"], symbol_len)
    return [waveform, info]