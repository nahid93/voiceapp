import os

mp3s = sorted(
    [f for f in os.listdir(".")
     if f.startswith("chunk_") and f.endswith(".mp3")]
)

with open("list.txt", "w") as f:
    for mp3 in mp3s:
        f.write(f"file '{mp3}'\n")

print("list.txt created")
