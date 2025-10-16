# run_batch.py
import os, sys, subprocess, glob
import numpy as np

# --- make matplotlib save even in headless shells ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from PIL import Image, ImageOps
from scipy import signal

VIDEO_PATH = "badapple.mp4"
FRAME_DIR = "frames"
SPEC_DIR  = "output_spectrograms"

os.makedirs(FRAME_DIR, exist_ok=True)
os.makedirs(SPEC_DIR,  exist_ok=True)

# 1) Extract frames with FFmpeg (silence banner; overwrite)
print("Extracting frames with FFmpeg...")
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-i", VIDEO_PATH, os.path.join(FRAME_DIR, "frame_%04d.png")
], check=True)
print("✓ Frames extracted.")

# 2) Batch over frames using original logic
fs = 48000                           # Sampling rate
low, high = 100, 12000               # Frequency mapping range (Hz)
duration_per_col = 0.05              # seconds per image column

frame_paths = sorted(glob.glob(os.path.join(FRAME_DIR, "frame_*.png")))
if not frame_paths:
    print("No frames found in ./frames — check VIDEO_PATH and permissions.")
    sys.exit(1)

for idx, frame_path in enumerate(frame_paths, 1):
    try:
        # --- 1. Load and preprocess image  ---
        img = Image.open(frame_path)
        gray = ImageOps.grayscale(img)
        gray = gray.resize((256, 128))       # width × height (tweak as needed)
        data = np.array(gray).astype(np.float32) / 255.0
        data = np.flipud(data)               # Flip vertically so top = high freq

        # --- 2. Define signal parameters (YOUR code) ---
        rows, cols = data.shape
        freqs = np.linspace(low, high, rows) # Map each row to a frequency

        # --- 3. Time mapping ---
        samples_per_col = int(duration_per_col * fs)
        t = np.linspace(0, duration_per_col, samples_per_col, endpoint=False)

        # --- 4. Encode image into signal ---
        signal_out = np.zeros(0, dtype=np.float32)
        for col in range(cols):
            frame_sig = np.zeros(samples_per_col, dtype=np.float32)
            for r, f_hz in enumerate(freqs):
                amp = data[r, col]
                if amp != 0.0:
                    frame_sig += amp * np.sin(2 * np.pi * f_hz * t)
            signal_out = np.concatenate((signal_out, frame_sig), axis=0)

        # --- 5. Spectrogram visualization ---
        f_vals, t_spec, Sxx = signal.spectrogram(
            signal_out,
            fs,
            nperseg=512,        # Smaller = better time detail
            noverlap=128,
            scaling="density"
        )

        plt.figure(figsize=(10, 6))
        plt.pcolormesh(t_spec, f_vals, 10 * np.log10(Sxx + 1e-10),
                       cmap="gray", shading="gouraud")
        plt.title("Bad Apple!! — Spectrogram Encoding")
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.ylim([low, high])
        plt.colorbar(label="Power [dB]")
        plt.tight_layout()

        out_png = os.path.join(SPEC_DIR, f"spec_{idx:04d}.png")
        plt.savefig(out_png, dpi=120)
        plt.close()

        if idx % 50 == 0:
            print(f"Saved {out_png}")

    except Exception as e:
        # Surface the exact frame that failed
        print(f"[ERROR] Frame {idx} ({frame_path}) failed: {e}")
        raise

print(f"Done. Spectrograms saved in: {os.path.abspath(SPEC_DIR)}")
