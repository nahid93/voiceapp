from gtts import gTTS
import glob
import os
import subprocess

print("Cleaning old files...")

for f in glob.glob("chunk_*.txt"):
    os.remove(f)

for f in glob.glob("chunk_*.mp3"):
    os.remove(f)

if os.path.exists("list.txt"):
    os.remove("list.txt")

if os.path.exists("final_story.mp3"):
    os.remove("final_story.mp3")

print("Step 1: Reading story...")

with open("story.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunk_size = 3000

chunks = [
    text[i:i + chunk_size]
    for i in range(0, len(text), chunk_size)
]

print(f"Total chunks: {len(chunks)}")

print("Step 2: Creating chunks...")

for index, chunk in enumerate(chunks, start=1):

    filename = f"chunk_{index:03}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(chunk)

print("Step 3: Generating audio...")

files = sorted(glob.glob("chunk_*.txt"))

total = len(files)

for num, file in enumerate(files, start=1):

    print(f"[{num}/{total}] {file}")

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    tts = gTTS(
        text=text,
        lang="hi"
    )

    mp3_name = file.replace(".txt", ".mp3")

    tts.save(mp3_name)

print("Audio generation complete")

print("Step 4: Creating merge list...")

mp3s = sorted(glob.glob("chunk_*.mp3"))

with open("list.txt", "w") as f:

    for mp3 in mp3s:
        f.write(f"file '{mp3}'\n")

print("Step 5: Merging audio...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "list.txt",
    "-c",
    "copy",
    "final_story.mp3"
])

print("")
print("Done!")
print("Output: final_story.mp3")
