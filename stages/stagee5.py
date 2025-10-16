# --- Imports ---
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io.wavfile import write

# --- 1. Load and preprocess image ---
img = Image.open("badapple.png")     # Your input image
gray = ImageOps.grayscale(img)
gray = gray.resize((256, 128))       # width × height (tweak as needed)
data = np.array(gray).astype(np.float32) / 255.0
data = np.flipud(data)               # Flip vertically so top = high freq

# --- 2. Define signal parameters ---
fs = 48000                           # Sampling rate
low, high = 100, 12000               # Frequency mapping range (Hz)
rows, cols = data.shape
freqs = np.linspace(low, high, rows) # Map each row to a frequency

# --- 3. Time mapping ---
duration_per_col = 0.05              # seconds per image column
samples_per_col = int(duration_per_col * fs)
t = np.linspace(0, duration_per_col, samples_per_col, endpoint=False)

# --- 4. Encode image into signal ---
signal_out = np.zeros(0)

for col in range(cols):
    frame = np.zeros(samples_per_col)
    for r, f in enumerate(freqs):
        amp = data[r, col]
        frame += amp * np.sin(2 * np.pi * f * t)
    signal_out = np.concatenate((signal_out, frame))

# --- 5. Spectrogram visualization ---
f, t_spec, Sxx = signal.spectrogram(
    signal_out,
    fs,
    nperseg=512,        # Smaller = better time detail
    noverlap=128,
    scaling="density"
)

plt.figure(figsize=(10, 6))
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx + 1e-10),
               cmap="gray", shading="gouraud")
plt.title("Bad Apple!! — Spectrogram Encoding")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.ylim([low, high])
plt.colorbar(label="Power [dB]")
plt.tight_layout()
plt.show()
