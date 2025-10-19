# Bad Apple!! but I animated it using Spectrograms

This is a personal project where I re-created **Bad Apple!!** using spectrograms. 

---

## See It

- **Video:** ![Bad Apple Spectrogram](badapplegiif.gif)(https://www.youtube.com/watch?v=PvIkpahSdOw)

- **Build Notes (Notion):** https://www.notion.so/Bad-Apple-Project-28a40e3f4f9380ff937af5771b81958c?source=copy_link
- **Build Notes (PDF):** [View my Bad Apple notes (PDF)](bad_apple_notes.pdf)

## What’s “Bad Apple!!”?

**Bad Apple!!** is a black-and-white shadow-style animation that’s become an internet classic. Over the years, people have rebuilt it in every way imaginable, ASCII art, Minecraft redstone, Desmos, oscilloscopes, calculators, printers, apples, Roblox, anything you can imagine, it's probably been animated.
https://www.youtube.com/watch?v=FtutLA63Cp8

Also check out this video
https://www.youtube.com/watch?v=6QY4ekac1_Q&pp=ygUQYmFkIGFwcGxlIG9yaWdpbg%3D%3D

---

## Why I Did This

I’m currently working with RF signals and spectrograms at Purdue, so I wanted to see if I could “re-animate” Bad Apple!! through that lens. Instead of pixels on a screen, I map visuals into the time–frequency world and then render them as spectrogram frames.

---
## How it works
My Bad Apple Spectrogram project works by taking each frame of the Bad Apple music video and turning it into sound, then visualizing that sound as a spectrogram. The idea is that an image can be represented as a matrix of brightness values, and those brightness values can be mapped to sound frequencies. I start by extracting each frame using FFmpeg, then I load the frame in Python using Pillow and convert it to grayscale so I only have to work with brightness instead of full RGB color. I normalize the brightness values between 0 and 1, where 0 represents a dark pixel and 1 represents a bright one.

Once I have that data, I iterate through the image column by column, from left to right, and within each column from top to bottom. Each pixel’s position in the column determines its frequency where pixels at the top correspond to higher frequencies, and pixels at the bottom correspond to lower ones. The brightness of the pixel controls how loud that frequency plays. For each column, I generate a short snippet of audio by adding together sine waves at the frequencies corresponding to the pixel rows, scaling each one by its brightness. Each snippet is about 0.05 seconds long, or 2,400 samples at a 48 kHz sampling rate.

After doing this for every column, I combine all those short snippets into one long waveform that represents the entire frame. Then, by running a Fourier Transform on that waveform, I can visualize how the frequencies change over time. The resulting spectrogram ends up redrawing the original image, since the brightness and frequency relationships in the sound directly correspond to those in the frame.

---

## What I Actually Did 

- Took the original Bad Apple!! video and broke it into frames.
- Turned each frame into a spectrogram-style image (brightness ≈ energy).
- Lined up all those spectrogram frames back into a video.
- Laid the original audio on top for sync.

The end result looks like a moving wall of frequencies—recognizably Bad Apple!!, but “spelled out” in the language of spectrograms. 

---

## What I Learned

- Spectrograms are a great bridge between pictures and sound—enough structure to be legible, enough softness to feel organic.
- Small choices (image height, window size, overlap) change the look a lot; there’s a spot where it reads clearly without looking clinical. The greatest example of this is the Time vs Frequency trade off, which are mentioned in my notes.
- Recreating a meme in a new medium is a fun way to test understanding without taking yourself too seriously (and have fun!). It's honestly nice to take a break from coursework to work on something you find fun in.


---

## Credits

- Original **“Bad Apple!!”** belongs to its creators.
- This remake is just for learning, fun, and showing what spectrograms can do.

— **Johnny Nguyen** • Purdue University CS • https://github.com/jnguyen727
