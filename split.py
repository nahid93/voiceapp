# split.py

with open("story.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunk_size = 1000

chunks = [
    text[i:i+chunk_size]
    for i in range(0, len(text), chunk_size)
]

for index, chunk in enumerate(chunks, start=1):
    filename = f"chunk_{index:03}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(chunk)

print(f"Total chunks created: {len(chunks)}")
