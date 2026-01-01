from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------- Read file ----------
with open("Sunbeam_internship_data.txt", "r", encoding="utf-8") as f:
    text = f.read()

# ---------- Recursive Text Splitter ----------
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n"],   # IMPORTANT: split by dropdown blocks
    chunk_size=600,       # large enough to keep one dropdown together
    chunk_overlap=100
)

chunks = splitter.split_text(text)

# ---------- Print chunks ----------
for i, chunk in enumerate(chunks, 1):
    print(f"\n================ CHUNK {i} =================")
    print(chunk)

# ---------- OPTIONAL: Save each chunk ----------
for i, chunk in enumerate(chunks, 1):
    with open(f"chunk_{i}.txt", "w", encoding="utf-8") as f:
        f.write(chunk)
