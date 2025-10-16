import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# --- Chirp Signal Setup ---
fs = 48000
t = np.linspace(0, 1, fs, endpoint=False)
sig = np.sin(2 * np.pi * (100 + 1900*t) * t)  # chirp: 100 Hz → 2000 Hz

# --- Add Gaussian Noise ---
sig_noisy = sig + 0.1 * np.random.randn(len(t))  # 0.1 controls noise level

# --- Compute Spectrogram ---
f, tt, Sxx = signal.spectrogram(sig_noisy, fs, nperseg=1024, noverlap=512, mode='psd')

# --- Convert to Decibels ---
Sxx_dB = 10 * np.log10(Sxx + 1e-10)

# --- Plot Spectrogram ---
plt.figure(figsize=(10, 5))
plt.pcolormesh(tt, f, Sxx_dB, shading="gouraud", cmap="inferno", vmin=-100, vmax=0)
plt.title("Spectrogram with Added Noise (Power Spectral Density, dB scale)")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.colorbar(label="Power [dB]")
plt.tight_layout()
plt.show()
