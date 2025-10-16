import subprocess
import re
import os

# --- Configuration ---
frames_dir = "output_spectrograms"     # Folder containing all spectrogram images
frames_pattern = os.path.join(frames_dir, "spec_%04d.png")
source_video = "badapple.mp4"  # Original Bad Apple video (with audio)
temp_video = "temp_no_audio.mp4"
output_video = "bad_apple_final.mp4"

# --- 1. Detect original FPS ---
print("🎞️ Detecting frame rate from source video...")
probe = subprocess.run(
    ["ffmpeg", "-i", source_video],
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)
match = re.search(r"(\d+(?:\.\d+)?) fps", probe.stderr)
if match:
    fps = float(match.group(1))
    print(f"✅ Detected FPS: {fps}")
else:
    fps = 30.0
    print("⚠️ Could not detect FPS. Defaulting to 30 FPS.")

# --- 2. Combine frames into a silent video ---
print("🎬 Combining spectrogram frames into silent video...")
subprocess.run([
    "ffmpeg",
    "-framerate", str(fps),
    "-i", frames_pattern,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    temp_video
], check=True)

# --- 3. Extract audio from the original video ---
print("🎧 Extracting audio from source video...")
subprocess.run([
    "ffmpeg",
    "-i", source_video,
    "-q:a", "0",
    "-map", "a",
    "bad_apple_audio.mp3"
], check=True)

# --- 4. Merge spectrogram video + audio ---
print("🎼 Merging spectrogram video with original audio...")
subprocess.run([
    "ffmpeg",
    "-i", temp_video,
    "-i", "bad_apple_audio.mp3",
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    output_video
], check=True)

# --- 5. Cleanup temporary files ---
os.remove(temp_video)
os.remove("bad_apple_audio.mp3")

print(f"✅ Done! Final synced video saved as: {output_video}")
