# --- Imports ---
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

# --- 1. Load image and convert to grayscale ---
im = Image.open("image.png")                  # Replace with your image path
grayscale = ImageOps.grayscale(im)            # Convert to grayscale (0–255)
grayscale.show()                              # Optional: preview grayscale image

# --- 2. Convert to NumPy array, flatten, and normalize ---
img_array = np.array(grayscale)               # Convert to 2-D NumPy array
flattened_img = img_array.flatten()           # Flatten to 1-D
normalized_img = flattened_img.astype(np.float32) / 255.0  # Normalize to [0, 1]

# --- 3. Create a 1 kHz carrier of the same length ---
fs = 48000                                    # Sampling rate
fc = 1000                                     # Carrier frequency (1 kHz)
t = np.arange(len(normalized_img)) / fs       # Time vector (seconds)
carrier = np.sin(2 * np.pi * fc * t)          # Carrier sine wave

# --- 4. Perform amplitude modulation using image brightness ---
am_signal = (normalized_img + 1) * carrier    # AM waveform

# --- 5. Plot a short segment to visualize the modulation ---
plt.figure(figsize=(10, 5))
plt.plot(t[:2000], am_signal[:2000], color='blue')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Image-Encoded Amplitude-Modulated Signal (1 kHz Carrier)')
plt.grid(True)
plt.tight_layout()
plt.show()
