import numpy as np
from py3gpp.nrOFDMInfo import nrOFDMInfo

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
    slot = 0
    grid = np.zeros((nrb * 12, 0), "complex")
    while idx + Nfft < waveform.shape[0]:
        if slot == 0 or slot == 7 * 2 ** (mu):
            cp = N_cp1
        else:
            cp = N_cp2
        slot = (slot + 1) % (7 * 2 ** (mu))
        cp_advance = int(CyclicPrefixFraction * cp)
        idx += cp_advance
        symbol_t = waveform[idx:][:Nfft]
        symbol_f = np.fft.fftshift(np.fft.fft(symbol_t))
        symbol_f *= np.exp(1j*2*np.pi*(cp - cp_advance)/Nfft*np.arange(len(symbol_f)))
        symbol_f = symbol_f[Nfft // 2 - nrb * 12 // 2 : Nfft // 2 + nrb * 12 // 2]
        grid = np.concatenate((grid, np.expand_dims(symbol_f, 1)), axis=1)
        idx += Nfft + (cp - cp_advance)
    return grid
