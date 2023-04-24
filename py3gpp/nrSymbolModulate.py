
# 38.211 5.1 Modulation mapper

import numpy as np

def nrSymbolModulate(databits, modulation):
    int_modtype = modulation.lower()

    assert int_modtype in ['bpsk_pi2', 'bpsk', 'qpsk', 'qam16', 'qam64', 'qam256'], "modulation type is incorrect"
    assert len(databits) > 0, "length of databits must be greater 0"
    assert max(databits) < 2 and min(databits) >= 0, "databits must be list of 0s and 1s"

    if int_modtype == 'bpsk':
        res_arr = np.zeros(len(databits), dtype=(complex))
        for idx, sample in enumerate(databits):
            res_arr[idx] = (1-2*sample) + 1j*(1-2*sample)
        res_arr = [x/np.sqrt(2) for x in res_arr]

    elif int_modtype == 'bpsk_pi2':
        res_arr = np.zeros(len(databits), dtype=(complex))
        for idx, sample in enumerate(databits):
            if idx%2:
                res_arr[idx] = (2*sample-1) + 1j*(1-2*sample)
            else:
                res_arr[idx] = (1-2*sample) + 1j*(1-2*sample)
        res_arr = [x/np.sqrt(2) for x in res_arr]

    elif int_modtype == 'qpsk':
        assert not (len(databits) % 2), "length of databits must be multiple of 2"
        res_arr = np.zeros((len(databits)//2), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//2)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = (1-2*sample[0]) + 1j*(1-2*sample[1])
        res_arr = [x/np.sqrt(2) for x in res_arr]

    elif int_modtype == 'qam16':
        assert not (len(databits) % 4), "length of databits must be multiple of 4"
        res_arr = np.zeros((len(databits)//4), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//4)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = ( (1-2*sample[0]) * (2-(1-2*sample[2])) ) + 1j*( (1-2*sample[1]) * (2-(1-2*sample[3])) )
        res_arr = [x/np.sqrt(10) for x in res_arr]

    elif int_modtype == 'qam64':
        assert not (len(databits) % 6), "length of databits must be multiple of 6"
        res_arr = np.zeros((len(databits)//6), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//6)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = ( (1-2*sample[0]) * (4-(1-2*sample[2]) * (2-(1-2*sample[4]))) ) + 1j*( (1-2*sample[1]) * (4-(1-2*sample[3]) * (2-(1-2*sample[5]))) )
        res_arr = [x/np.sqrt(42) for x in res_arr]

    elif int_modtype == 'qam256':
        assert not (len(databits) % 8), "length of databits must be multiple of 8"
        res_arr = np.zeros((len(databits)//8), dtype=(complex))
        chunks = np.array_split(databits, len(databits)//8)
        for idx, sample in enumerate(chunks):
            res_arr[idx] = ( (1-2*sample[0]) * (8-(1-2*sample[2]) * (4-(1-2*sample[4]) * (2-(1-2*sample[6])))) ) + 1j*( (1-2*sample[1]) * (8-(1-2*sample[3]) * (4-(1-2*sample[5]) * (2-(1-2*sample[7])))) )
        res_arr = [x/np.sqrt(170) for x in res_arr]

    return res_arr
