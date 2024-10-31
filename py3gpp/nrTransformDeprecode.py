import numpy as np

def nrTransformDeprecode(modSym, mrb):
    mrb = int(mrb)
    assert modSym.shape[0] % (mrb * 12) == 0, "input number of rows must be an integer multiple of mrb * 12"
    return (np.fft.ifft(modSym.reshape(int(modSym.shape[0] / (mrb * 12)), mrb * 12)) * np.sqrt(mrb * 12)).ravel()
