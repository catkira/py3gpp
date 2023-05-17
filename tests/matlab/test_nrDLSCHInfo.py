import matlab.engine
import itertools
import numpy as np
import pytest

from py3gpp.nrDLSCHInfo import nrDLSCHInfo

def run_nr_dlsch_info(tbs, tcr, eng):
    ref_data = eng.nrDLSCHInfo(matlab.double(tbs), matlab.double(tcr))
    # print(ref_data)

    data = nrDLSCHInfo(tbs, tcr)

    assert np.all(ref_data == data)

@pytest.mark.parametrize("tbs", [0, 1, 100, 3824, 6666])
@pytest.mark.parametrize("tcr", [0.1, 0.25, 0.67, 0.99])
def test_nr_dlsch_info(tbs, tcr):
    eng = matlab.engine.connect_matlab()

    try:
        run_nr_dlsch_info(tbs, tcr, eng)
    finally:
        eng.quit()

if __name__ == '__main__':
    test_nr_dlsch_info(1, 0.1)