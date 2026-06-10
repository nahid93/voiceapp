import asyncio
import edge_tts
import glob
import os
import subprocess
import time
import sys
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

VOICE_NAME = "hi-IN-MadhurNeural"

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

menu = Table(title="Main Menu")

menu.add_column("Option")
menu.add_column("Action")

menu.add_row("1", "Generate Story Audio")
menu.add_row("2", "Voice Settings")
menu.add_row("3", "Preview Voice")
menu.add_row("4", "Output History")
menu.add_row("5", "Download Last Output")
menu.add_row("6", "Play Last Output")
menu.add_row("7", "Exit")

console.print(menu)

main_choice = input("Select Option (1-7): ").strip()

if main_choice == "7":

    exit()

if main_choice == "4":

    print("\nRecent Outputs:\n")

    files = sorted(
        glob.glob("output/*.mp3"),
        key=os.path.getmtime,
        reverse=True
    )

    if not files:
        print("No output files found.")

    else:

        for i, file in enumerate(files[:10], start=1):

            size = os.path.getsize(file) / (1024 * 1024)

            print(
                f"{i}. {os.path.basename(file)} "
                f"({size:.1f} MB)"
            )

if main_choice == "6":

    files = sorted(
        glob.glob("output/*.mp3"),
        key=os.path.getmtime,
        reverse=True
    )

    if not files:

        print("No output found.")

    else:

        latest = files[0]

        print(
            f"\nPlaying: "
            f"{os.path.basename(latest)}"
        )

        subprocess.run([
            "termux-open",
            latest
        ])

    exit()

if main_choice == "5":

    files = sorted(
        glob.glob("output/*.mp3"),
        key=os.path.getmtime,
        reverse=True
    )

    if not files:

        print("No output found.")

    else:

        latest = files[0]

        download_path = (
            "/storage/emulated/0/Download/"
            + os.path.basename(latest)
        )

        subprocess.run([
            "cp",
            latest,
            download_path
        ])

        print(
            "\nDownloaded to:\n"
            + download_path
        )

if main_choice == "2":

    print("\nVoice Settings")

    print("1. MadhurNeural")
    print("2. SwaraNeural")
    print("3. Custom Voice")

    voice_choice = input("Choose: ").strip()

    if voice_choice == "1":
        VOICE_NAME = "hi-IN-MadhurNeural"

    elif voice_choice == "2":
        VOICE_NAME = "hi-IN-SwaraNeural"

    elif voice_choice == "3":
        VOICE_NAME = input(
            "Enter Edge-TTS Voice Name: "
        ).strip()

    print(f"\nCurrent Voice: {VOICE_NAME}")
    exit()

if main_choice == "3":

    print("\nPreview Voice")

    print("1. Preview Current Voice")
    print("2. MadhurNeural")
    print("3. SwaraNeural")
    print("4. Custom Voice")

    preview_choice = input("Choose: ").strip()

    if preview_choice == "1":
        preview_voice = VOICE_NAME

    elif preview_choice == "2":
        preview_voice = "hi-IN-MadhurNeural"

    elif preview_choice == "3":
        preview_voice = "hi-IN-SwaraNeural"

    elif preview_choice == "4":
        preview_voice = input(
            "Enter Voice Name: "
        ).strip()

    else:
        exit()

    preview_text = (
        "नमस्ते दोस्तों। "
        "यह एक डेमो वॉइस प्रीव्यू है। "
        "आपका AI Story Generator तैयार है।"
    )

    print("\nGenerating Preview...\n")

    communicate = edge_tts.Communicate(
        text=preview_text,
        voice=preview_voice
    )

    asyncio.run(
        communicate.save(
            "output/preview.mp3"
        )
    )

    subprocess.run([
        "termux-open",
        "output/preview.mp3"
    ])

    exit()

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

voice_table = Table(title="Voice Selection")

voice_table.add_column("Option")
voice_table.add_column("Voice")

voice_table.add_row("1", "MadhurNeural")
voice_table.add_row("2", "SwaraNeural")
voice_table.add_row("3", "Custom")

console.print(voice_table)

voice_choice = input("Select Voice (1-3): ").strip()

if voice_choice == "1":
    VOICE_NAME = "hi-IN-MadhurNeural"

elif voice_choice == "2":
    VOICE_NAME = "hi-IN-SwaraNeural"

elif voice_choice == "3":
    VOICE_NAME = input(
        "Enter Edge-TTS Voice Name: "
    ).strip()

else:
    VOICE_NAME = "hi-IN-MadhurNeural"

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

DOWNLOAD_DIR = (
    "/storage/emulated/0/Download/Adnan Story"
)

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)

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

print("\nStory Input Mode")
print("1. Use story.txt")
print("2. Paste Story Here")

story_mode = input("Choose (1-2): ").strip()

try:

    if story_mode == "2":

        print("\nPaste your story below.")
        print("Type END on a new line when finished.\n")

        lines = []

        while True:

            line = input()

            if line.strip() == "END":
                break

            lines.append(line)

        text = "\n".join(lines)

    else:

        with open(
            "story.txt",
            "r",
            encoding="utf-8"
        ) as f:

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
            voice=VOICE_NAME,
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

download_file = os.path.join(
    DOWNLOAD_DIR,
    os.path.basename(final_mp3)
)

subprocess.run([
    "cp",
    final_mp3,
    download_file
])

final_mp3 = download_file

print("")
print("[1] Open File")
print("[2] Share File")
print("[3] Exit")

share_choice = input(
    "Choose: "
).strip()

if share_choice == "1":

    subprocess.run([
        "termux-open",
        final_mp3
    ])

elif share_choice == "2":

    subprocess.run([
        "termux-open",
        final_mp3
    ])

elif share_choice == "3":

    os.execl(
        sys.executable,
        sys.executable,
        *sys.argv
    )

print("")
print(
    f"Output: "
    f"{final_mp3}"
)

