import numpy as np
import pytest
from py3gpp.nrLDPCEncode import nrLDPCEncode
from py3gpp.nrLDPCDecode import nrLDPCDecode
from py3gpp.nrSymbolModulate import nrSymbolModulate
from py3gpp.nrSymbolDemodulate import nrSymbolDemodulate


def ldpc_awgn_simulation(bgn, K, F, EbN0_dB, num_frames=10, maxNumIter=10):
    """Simulate LDPC encode -> QPSK modulate -> AWGN -> QPSK demodulate -> LDPC decode.

    Returns (BER, FER).
    """
    C = 1  # one code block per frame

    total_bit_errors = 0
    total_info_bits = 0
    frame_errors = 0

    for _ in range(num_frames):
        # 1. Generate random test data with filler bits
        info_bits = np.random.randint(2, size=(K - F, C))
        fillers = -1 * np.ones((F, C))
        cbs = np.vstack((info_bits, fillers))

        # 2. LDPC encode
        coded_cbs = nrLDPCEncode(cbs.copy(), bgn)
        N = coded_cbs.shape[0]
        code_rate = K / N

        # Track filler positions in coded output
        filler_mask = coded_cbs[:, 0] == -1

        # Prepare bits for modulation (replace fillers with 0)
        tx_bits = coded_cbs[:, 0].copy()
        tx_bits[filler_mask] = 0

        # 3. QPSK modulate
        symbols = nrSymbolModulate(tx_bits.astype(int), 'QPSK')

        # 4. Add AWGN noise
        EsN0_dB = EbN0_dB + 10 * np.log10(2 * code_rate)
        nVar = 1.0 / (10 ** (EsN0_dB / 10))
        noise = np.sqrt(nVar / 2) * (
            np.random.randn(len(symbols)) + 1j * np.random.randn(len(symbols))
        )
        rx_symbols = symbols + noise

        # 5. QPSK demodulate (soft decision)
        soft_bits = nrSymbolDemodulate(rx_symbols, 'QPSK', nVar)

        # Set filler positions to 0 (erasure — no information)
        soft_bits[filler_mask] = 0

        # Reshape for LDPC decoder input (N x C)
        soft_bits_2d = soft_bits.reshape(-1, 1)

        # 6. LDPC decode
        decoded, niters = nrLDPCDecode(soft_bits_2d, bgn, maxNumIter)

        # 7. Compute errors on information bits (exclude fillers)
        tx_info = cbs[:K - F, 0]
        rx_info = decoded[:K - F, 0]

        bit_errors = int(np.sum(tx_info != rx_info))
        total_bit_errors += bit_errors
        total_info_bits += (K - F)
        if bit_errors > 0:
            frame_errors += 1

    BER = total_bit_errors / total_info_bits
    FER = frame_errors / num_frames
    return BER, FER


@pytest.mark.parametrize("bgn, K, F", [(2, 2560, 36)])
@pytest.mark.parametrize("EbN0_dB", [5])
def test_nrLDPCDecode_BER(bgn, K, F, EbN0_dB):
    """Verify LDPC decode produces zero errors at high SNR through the full pipeline."""
    np.random.seed(42)
    BER, FER = ldpc_awgn_simulation(bgn, K, F, EbN0_dB, num_frames=10, maxNumIter=10)
    assert BER == 0, f"BER = {BER} at Eb/N0 = {EbN0_dB} dB (expected 0)"
    assert FER == 0, f"FER = {FER} at Eb/N0 = {EbN0_dB} dB (expected 0)"


if __name__ == '__main__':
    bgn = 2
    K = 2560
    F = 36
    Zc = K // 10
    N = Zc * 50
    num_frames = 100
    maxNumIter = 10

    print("LDPC BER/FER Benchmark")
    print(f"  Base graph: {bgn}")
    print(f"  K={K}, F={F}, N={N}, code rate={K / N:.3f}")
    print(f"  Frames per SNR point: {num_frames}")
    print(f"  Max decoder iterations: {maxNumIter}")
    print(f"  Modulation: QPSK")
    print()
    print(f"{'Eb/N0 (dB)':>12} {'BER':>12} {'FER':>12}")
    print("-" * 40)

    for EbN0_dB in np.arange(-1, 6, 1.0):
        np.random.seed(42)
        BER, FER = ldpc_awgn_simulation(bgn, K, F, EbN0_dB, num_frames=num_frames, maxNumIter=maxNumIter)
        print(f"{EbN0_dB:>12.1f} {BER:>12.6f} {FER:>12.4f}")
