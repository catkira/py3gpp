"""Generate BER/FER plot for nrLDPCDecode over AWGN channel with QPSK modulation."""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# allow importing from the tests directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tests.test_nrLDPCDecode_BER import ldpc_awgn_simulation

bgn = 2
K = 2560
F = 36
Zc = K // 10
N = Zc * 50
code_rate = K / N
num_frames = 100
maxNumIter = 10

EbN0_range = np.arange(-1, 6, 1.0)
ber_results = []
fer_results = []

print(f"LDPC BER/FER plot generation")
print(f"  bgn={bgn}, K={K}, F={F}, N={N}, rate={code_rate:.3f}, QPSK")
print(f"  {num_frames} frames per SNR point, max {maxNumIter} decoder iterations")
print()

for snr in EbN0_range:
    np.random.seed(42)
    BER, FER = ldpc_awgn_simulation(bgn, K, F, snr, num_frames=num_frames, maxNumIter=maxNumIter)
    ber_results.append(BER)
    fer_results.append(FER)
    print(f"  Eb/N0 = {snr:+.1f} dB  =>  BER = {BER:.6f},  FER = {FER:.4f}")

# Replace exact zeros with a tiny value so they show on log scale
ber_plot = [b if b > 0 else 1e-7 for b in ber_results]
fer_plot = [f if f > 0 else 1e-7 for f in fer_results]

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(EbN0_range, ber_plot, 'bo-', label='BER', markersize=6)
ax.semilogy(EbN0_range, fer_plot, 'rs--', label='FER', markersize=6)
ax.set_xlabel('Eb/N0 (dB)')
ax.set_ylabel('Error Rate')
ax.set_title(f'LDPC BER/FER — BG{bgn}, rate {code_rate:.2f}, QPSK, {num_frames} frames')
ax.legend()
ax.grid(True, which='both', linestyle='--', alpha=0.5)
ax.set_ylim(bottom=1e-5, top=1)

out_path = os.path.join(os.path.dirname(__file__), 'ldpc_ber_fer.png')
fig.savefig(out_path, dpi=150, bbox_inches='tight')
print(f"\nPlot saved to {out_path}")
