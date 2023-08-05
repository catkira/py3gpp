import numpy as np
import scipy
from py3gpp import nrOFDMModulate


def nrTimingEstimate(
    carrier=None,
    waveform=None,
    refGrid=None,
    nrb=None,
    scs=None,
    initialNSlot=None,
    refInd=None,
    refSym=None,
    CyclicPrefix="normal",
    Nfft=None,
    SampleRate=None,
    CarrierFrequency=None
):
    refWaveform, _ = nrOFDMModulate(
        grid=refGrid, scs=scs, initialNSlot=initialNSlot, SampleRate=SampleRate, Nfft=Nfft, carrier=carrier, CarrierFrequency=CarrierFrequency
    )
    xcorr = scipy.signal.correlate(waveform, refWaveform, "valid")
    index = np.argmax(np.abs(xcorr))
    return index
