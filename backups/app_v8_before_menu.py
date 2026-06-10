import asyncio
import edge_tts
import glob
import os
import subprocess
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# =========================
# SETTINGS
# =========================

CHUNK_SIZE = 3000

console.print(
    Panel(
        "[bold cyan]AI Story Generator V6[/bold cyan]\n"
        "[yellow]Edge-TTS MadhurNeural Edition[/yellow]\n"
        "[green]TTS By Adnan Ahammed Nahid[/green]",
        title="Welcome",
        expand=False
    )
)

speed_table = Table(title="Voice Speed")

speed_table.add_column("Option")
speed_table.add_column("Speed")

speed_table.add_row("1", "Slow")
speed_table.add_row("2", "Normal")
speed_table.add_row("3", "Fast")

console.print(speed_table)

choice = input("Select Speed (1-3): ").strip()

style_table = Table(title="Voice Style")

style_table.add_column("Option")
style_table.add_column("Style")

style_table.add_row("1", "Normal")
style_table.add_row("2", "Storytelling")
style_table.add_row("3", "Dramatic")

console.print(style_table)

style_choice = input("Select Style (1-3): ").strip()

if style_choice == "1":
    VOICE_RATE = "-5%"
    VOICE_PITCH = "+2Hz"
    STYLE_NAME = "Normal"

elif style_choice == "2":
    VOICE_RATE = "-15%"
    VOICE_PITCH = "+4Hz"
    STYLE_NAME = "Storytelling"

elif style_choice == "3":
    VOICE_RATE = "-20%"
    VOICE_PITCH = "+6Hz"
    STYLE_NAME = "Dramatic"

else:
    VOICE_RATE = "-5%"
    VOICE_PITCH = "+2Hz"
    STYLE_NAME = "Normal"

speed_map = {
    "1": 0.9,
    "2": 1.0,
    "3": 1.2
}

VOICE_SPEED = speed_map.get(choice, 1.0)

os.makedirs("output", exist_ok=True)
# =========================
# CLEAN OLD CHUNKS
# =========================

for f in glob.glob("chunk_*.txt"):

    try:
        os.remove(f)
    except:
        pass

for f in glob.glob("output/chunk_*.mp3"):

    try:
        os.remove(f)
    except:
        pass

if os.path.exists("output/list.txt"):

    try:
        os.remove("output/list.txt")
    except:
        pass

start_time = time.time()

# =========================
# READ STORY
# =========================

try:

    with open("story.txt", "r", encoding="utf-8") as f:
        text = f.read()

except FileNotFoundError:

    print("")
    print("ERROR: story.txt not found")
    exit()

char_count = len(text)

print("")
print(f"Characters: {char_count}")

estimated_minutes = max(
    1,
    round(char_count / 800)
)

print(
    f"Estimated Duration: "
    f"{estimated_minutes} min"
)

# =========================
# SMART SPLIT
# =========================

print("")
print("Smart splitting...")

sentences = (
    text
    .replace("\n", " ")
    .split("।")
)

chunks = []
current = ""

for sentence in sentences:

    sentence = sentence.strip()

    if not sentence:
        continue

    sentence = sentence + "।"

    if (
        len(current)
        + len(sentence)
        < CHUNK_SIZE
    ):

        current += sentence + " "

    else:

        chunks.append(
            current.strip()
        )

        current = sentence + " "

if current.strip():

    chunks.append(
        current.strip()
    )

print(
    f"Total Chunks: "
    f"{len(chunks)}"
)

for index, chunk in enumerate(
    chunks,
    start=1
):

    filename = (
        f"chunk_{index:03}.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(chunk)
# =========================
# GENERATE AUDIO
# =========================

print("")
print("Generating audio...")

total = len(chunks)

for num in range(
    1,
    total + 1
):

    txt_file = (
        f"chunk_{num:03}.txt"
    )

    mp3_file = (
        f"output/chunk_{num:03}.mp3"
    )

    percent = int(
        (num / total) * 100
    )

    elapsed = (
        time.time()
        - start_time
    )

    if num > 1:

        avg = elapsed / (num - 1)

        eta = int(
            avg *
            (total - num + 1)
        )

    else:

        eta = 0

    print("")
    print(
        f"[{num}/{total}] "
        f"{percent}%"
    )

    print(
        f"ETA: {eta} sec"
    )

    # Resume Mode

    if os.path.exists(
        mp3_file
    ):

        print(
            "Already exists"
        )

        continue

    with open(
        txt_file,
        "r",
        encoding="utf-8"
    ) as f:

        chunk_text = (
            f.read()
        )

    success = False

    # Retry System

    for attempt in range(
        1,
        4
    ):

        try:

            print(
                f"Attempt "
                f"{attempt}/3"
            )
            communicate = edge_tts.Communicate(
            text=chunk_text,
            voice="hi-IN-MadhurNeural",
            rate=VOICE_RATE,
            pitch=VOICE_PITCH
            ) 

            asyncio.run(
                communicate.save(
                    mp3_file
                )
            )

            success = True
            break

        except Exception as e:

            print(
                "Retrying..."
            )

            time.sleep(2)

    if not success:

        print("")
        print(
            "FAILED:"
        )

        print(txt_file)

        exit()

# =========================
# CREATE OUTPUT HISTORY
# =========================

print("")
print("Creating output history...")

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

final_mp3 = (
    f"output/story_{timestamp}.mp3"
)

# =========================
# CREATE MERGE LIST
# =========================

with open(
    "output/list.txt",
    "w"
) as f:

    mp3s = sorted(
        glob.glob(
            "output/chunk_*.mp3"
        )
    )

    for mp3 in mp3s:

        f.write(
            f"file '../{mp3}'\n"
        )

# =========================
# MERGE AUDIO
# =========================

print("")
print("Merging audio...")

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
    final_mp3
])

# =========================
# SPEED CONTROL
# =========================

if VOICE_SPEED != 1.0:

    print("")
    print(
        "Applying speed..."
    )

    speed_file = (
        final_mp3.replace(
            ".mp3",
            "_speed.mp3"
        )
    )

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        final_mp3,
        "-filter:a",
        f"atempo={VOICE_SPEED}",
        speed_file
    ])

    final_mp3 = speed_file

# =========================
# FINAL STATS
# =========================

total_time = int(
    time.time()
    - start_time
)

minutes = (
    total_time // 60
)

seconds = (
    total_time % 60
)

print("")
print("================================")
print("DONE")
print("================================")
print("")

print(
    f"Characters: "
    f"{char_count}"
)

print(
    f"Chunks: "
    f"{len(chunks)}"
)

print(
    f"Time Taken: "
    f"{minutes}m "
    f"{seconds}s"
)
print("")
print("Converting to Android compatible MP3...")

compatible_mp3 = final_mp3.replace(
    ".mp3",
    "_compatible.mp3"
)

subprocess.run([
    "ffmpeg",
    "-y",
    "-i",
    final_mp3,
    "-ar", "44100",
    "-ac", "2",
    "-b:a", "128k",
    compatible_mp3
])

final_mp3 = compatible_mp3
print("")
print(
    f"Output: "
    f"{final_mp3}"
)

