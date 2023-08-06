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
        carrier = nrCarrierConfig(1, NSizeGrid = nrb, NStartGrid = 0, SubcarrierSpacing = scs, NSlot = initialNSlot)
    else:
        nrb = carrier.NSizeGrid
        scs = carrier.SubcarrierSpacing
        initialNSlot = 0 if initialNSlot is None else initialNSlot
        
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
    N_cp = np.zeros(carrier.SymbolsPerSlot, dtype=int)
    for i in range(len(N_cp)):
        N_cp[i] = N_cp1 if i == 0 or i == 7 * 2 ** (mu) else N_cp2

    idx = 0
    sym_pos_in_slot = initialNSlot
    grid = np.zeros((nrb * 12, 0), "complex")

    sample_pos_in_slot = 0
    for i in range(initialNSlot):
        sample_pos_in_slot += Nfft + N_cp[i]

    symbols_per_slot = carrier.SymbolsPerSlot
    while idx + Nfft <= waveform.shape[0]:
        sym_pos_in_slot = sym_pos_in_slot % symbols_per_slot
        cp_advance = int(CyclicPrefixFraction * N_cp[sym_pos_in_slot])
        idx += cp_advance
        symbol_t = waveform[idx:][:Nfft]
        symbol_f = np.fft.fftshift(np.fft.fft(symbol_t))

        symbol_f *= np.exp(1j*2*np.pi*(N_cp[sym_pos_in_slot] - cp_advance)/Nfft*np.arange(len(symbol_f)))
        symbol_f *= np.exp(1j*np.pi*(N_cp[sym_pos_in_slot] - cp_advance))

        symbol_f = symbol_f[Nfft // 2 - nrb * 12 // 2 : Nfft // 2 + nrb * 12 // 2]

        # phase compensation according to TS 38.211 section 5.4
        if sym_pos_in_slot == 0:
            sample_pos_in_slot = 0
        sample_pos_in_slot += N_cp[sym_pos_in_slot]
        # print(f'symbol {sym_pos_in_slot}, pos {sample_pos_in_slot}, CP {N_cp[sym_pos_in_slot]}, pos {idx - cp_advance}')
        symbol_f *= np.exp(1j * 2 * np.pi * CarrierFrequency / SampleRate * sample_pos_in_slot)
        sample_pos_in_slot += Nfft

        grid = np.concatenate((grid, np.expand_dims(symbol_f, 1)), axis=1)
        idx += Nfft + (N_cp[sym_pos_in_slot] - cp_advance)
        # print(f'slot {slot}, cp_len {N_cp}')
        sym_pos_in_slot = sym_pos_in_slot + 1
    return grid
