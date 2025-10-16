import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps


# Open image, convert to grayscale 

im = Image.open("image.png")
grayscale = ImageOps.grayscale(im)
grayscale.show()

# Convert the image to a Python array

img_array = np.array(grayscale)
# Flatten the image array

flattened_img = img_array.flatten()

# Normalize the array

normalized_img = flattened_img.astype('float32') / 255.0


# --- Signal parameters ---
fs = 48000            # Sampling rate (samples per second)
fc = 1000             # Carrier frequency (Hz)
fm = 5                # Modulating frequency (Hz)
duration = 1          # Signal length in seconds

# --- Time vector ---
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# --- Generate signals ---
carrier = np.sin(2 * np.pi * fc * t)         # High-frequency carrier
modulator = np.sin(2 * np.pi * fm * t)       # Slow modulating signal (controls amplitude)

# --- Perform amplitude modulation ---
# Add 1 so amplitude never goes negative (range 0 → 2)
modulated = (1 + modulator) * carrier

# --- Plot results ---
plt.figure(figsize=(10, 6))
plt.plot(t[:4800], modulated[:4800], color='blue', label='AM Signal')
plt.plot(t[:4800], 1 + modulator[:4800], color='red', label='Envelope (1 + modulator)', linewidth=2, alpha=0.7)
plt.title('Amplitude Modulation: 1 kHz Carrier, 5 Hz Modulator')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
