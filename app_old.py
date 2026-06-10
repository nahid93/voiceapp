from gtts import gTTS
import glob
import os
import subprocess

print("Step 1: Splitting story...")

with open("story.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunk_size = 1000

chunks = [
    text[i:i + chunk_size]
    for i in range(0, len(text), chunk_size)
]

for index, chunk in enumerate(chunks, start=1):

    filename = f"chunk_{index:03}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(chunk)

print(f"Created {len(chunks)} chunks")

print("Step 2: Generating audio...")

files = sorted(glob.glob("chunk_*.txt"))

for file in files:

    print("Processing:", file)

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    tts = gTTS(
        text=text,
        lang="hi"
    )

    mp3_name = file.replace(".txt", ".mp3")

    tts.save(mp3_name)

    print("Saved:", mp3_name)

print("Audio generation complete")

print("Step 3: Creating merge list...")

mp3s = sorted(
    [
        f
        for f in os.listdir(".")
        if f.startswith("chunk_")
        and f.endswith(".mp3")
    ]
)

with open("list.txt", "w") as f:

    for mp3 in mp3s:
        f.write(f"file '{mp3}'\n")

print("Step 4: Merging audio...")

subprocess.run([
    "ffmpeg",
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

print("Done!")
print("Output: final_story.mp3")
