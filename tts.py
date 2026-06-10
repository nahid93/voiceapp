from gtts import gTTS
import glob

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

print("All audio generated.")

