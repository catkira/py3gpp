import numpy as np
from py3gpp.nrOFDMInfo import nrOFDMInfo
from py3gpp.configs.nrCarrierConfig import nrCarrierConfig

# TODO: implement CyclicPrefixFraction
def nrOFDMDemodulate(
    carrier=None,
    waveform=None,
    nrb=None,
    scs=None,
    initialNSlot=None,
    CyclicPrefix="normal",
    Nfft=None,
    SampleRate=None,
    CarrierFrequency=0,
    CyclicPrefixFraction=0.5,
):
    if waveform is None:
        print("Error: no waveform given!")
        return
    if carrier is None:
        if nrb == None:
            print("Error: nrb is needed without carrierConfig!")
            return
        if scs == None:
            print("Error: scs is needed without carrierConfig!")
            return
        if initialNSlot == None:
            print("Error: initialNSlot is needed without carrierConfig!")
            return
        carrier = nrCarrierConfig(1, NSizeGrid = nrb, NStartGrid = 0, SubcarrierSpacing = scs)
    else:
        nrb = carrier.NSizeGrid
        scs = carrier.SubcarrierSpacing
        initialNSlot = 0
        
    if Nfft == None:
        if SampleRate == None:
            Nfft = nrOFDMInfo(nrb=nrb, scs=scs)["Nfft"]
            SampleRate = int(Nfft * scs * 1000)
        else:
            Nfft = int(SampleRate // scs // 1000)
    mu = (scs // 15) - 1
    if CyclicPrefix == "normal":
        N_cp1 = int(((144) * 2 ** (-mu) + 16) * (SampleRate / 30720000))
        N_cp2 = int((144 * 2 ** (-mu)) * (SampleRate / 30720000))
    else:
        N_cp1 = int((512 * 2 ** (-mu)) * (SampleRate / 30720000))
        N_cp2 = N_cp1

    idx = 0
    sym_pos_in_slot = initialNSlot
    grid = np.zeros((nrb * 12, 0), "complex")
    sample_pos_in_slot = 0
    symbols_per_slot = carrier.SymbolsPerSlot
    while idx + Nfft <= waveform.shape[0]:
        sym_pos_in_slot = sym_pos_in_slot % symbols_per_slot
        if sym_pos_in_slot == 0 or sym_pos_in_slot == 7 * 2 ** (mu):
            N_cp = N_cp1
        else:
            N_cp = N_cp2
        cp_advance = int(CyclicPrefixFraction * N_cp)
        idx += cp_advance
        symbol_t = waveform[idx:][:Nfft]
        symbol_f = np.fft.fftshift(np.fft.fft(symbol_t))

        symbol_f *= np.exp(1j*2*np.pi*(N_cp - cp_advance)/Nfft*np.arange(len(symbol_f)))
        symbol_f *= np.exp(1j*np.pi*(N_cp - cp_advance))

        symbol_f = symbol_f[Nfft // 2 - nrb * 12 // 2 : Nfft // 2 + nrb * 12 // 2]

        # phase compensation according to TS 38.211 section 5.4
        if sym_pos_in_slot == 0:
            sample_pos_in_slot = 0
        sample_pos_in_slot += N_cp
        symbol_f *= np.exp(1j * 2 * np.pi * CarrierFrequency / SampleRate * sample_pos_in_slot)
        sample_pos_in_slot += Nfft

        grid = np.concatenate((grid, np.expand_dims(symbol_f, 1)), axis=1)
        idx += Nfft + (N_cp - cp_advance)
        # print(f'slot {slot}, cp_len {N_cp}')
        sym_pos_in_slot = sym_pos_in_slot + 1
    return grid
