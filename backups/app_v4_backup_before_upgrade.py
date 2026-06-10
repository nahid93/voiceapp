from gtts import gTTS
import glob
import os
import subprocess
import time

os.makedirs("output", exist_ok=True)

print("Step 1: Reading story...")

with open("story.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunk_size = 3000

print("Step 2: Smart splitting...")

sentences = text.replace("\n", " ").split("।")

chunks = []
current = ""

for sentence in sentences:

    sentence = sentence.strip()

    if not sentence:
        continue

    sentence = sentence + "।"

    if len(current) + len(sentence) < chunk_size:
        current += sentence + " "
    else:
        chunks.append(current.strip())
        current = sentence + " "

if current.strip():
    chunks.append(current.strip())

print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):

    filename = f"chunk_{index:03}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(chunk)

print("Step 3: Generating audio...")

total = len(chunks)

for num in range(1, total + 1):

    txt_file = f"chunk_{num:03}.txt"
    mp3_file = f"output/chunk_{num:03}.mp3"

    if os.path.exists(mp3_file):
        print(f"[{num}/{total}] Skipped")
        continue

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    success = False

    for attempt in range(1, 4):

        try:

            print(f"[{num}/{total}] Attempt {attempt}")

            tts = gTTS(
                text=text,
                lang="hi"
            )

            tts.save(mp3_file)

            success = True
            break

        except Exception as e:

            print("Retrying...")
            time.sleep(2)

    if not success:
        print("Failed:", txt_file)
        exit()

print("Step 4: Creating merge list...")

mp3s = sorted(glob.glob("output/chunk_*.mp3"))

with open("output/list.txt", "w") as f:

    for mp3 in mp3s:
        f.write(f"file '../{mp3}'\n")

print("Step 5: Merging audio...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "output/list.txt",
    "-c",
    "copy",
    "output/final_story.mp3"
])

print("")
print("Done!")
print("Output: output/final_story.mp3")

