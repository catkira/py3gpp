import numpy as np
import pytest
from py3gpp.nrLDPCEncode import nrLDPCEncode
from py3gpp.nrCodeBlockSegmentLDPC import nrCodeBlockSegmentLDPC
from py3gpp.nrDLSCHInfo import nrDLSCHInfo
from py3gpp.nrCRCEncode import nrCRCEncode

@pytest.mark.parametrize("K", [2560])
@pytest.mark.parametrize("C", [1, 2, 3])
@pytest.mark.parametrize("F", [36])
@pytest.mark.parametrize("bgn", [2])
def test_nrLDPCEncode(K, C, F, bgn):
    cbs = np.random.randint(2, size = (K - F, C))
    fillers = (-1) * np.ones((F, C))
    cbs = np.vstack((cbs, fillers))
    codedcbs_1 = nrLDPCEncode(cbs.copy(), bgn, algo = 'sionna')
    codedcbs_2 = nrLDPCEncode(cbs.copy(), bgn, algo = 'thangaraj')
    assert np.array_equal(codedcbs_1, codedcbs_2)

def test_nrLDPCEncode_sionna_bg2_k640_valid_case():
    tbs = 552
    R = 120 / 1024

    info = nrDLSCHInfo(tbs, R)
    assert info["BGN"] == 2
    assert info["K"] == 640
    assert info["Zc"] == 64
    assert info["C"] == 1

    rng = np.random.default_rng(7)
    tb = rng.integers(0, 2, size=tbs, dtype=np.int8)
    tb_crc = nrCRCEncode(tb, info["CRC"])[:, 0].astype(np.int8)
    cbs = nrCodeBlockSegmentLDPC(tb_crc, info["BGN"])

    encoded = nrLDPCEncode(cbs, info["BGN"], algo="sionna")

    assert encoded.shape == (info["N"], info["C"])

if __name__ == '__main__':
    bgn = 2
    C = 2
    K = 2560
    F = 36
    test_nrLDPCEncode(K, C, F, bgn)
    test_nrLDPCEncode_sionna_bg2_k640_valid_case()
