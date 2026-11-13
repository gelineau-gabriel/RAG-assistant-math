import json
from pathlib import Path
from .config import WIKIPEDIA_PATH, CHUNKS_PATH

def split_text(text, chunk_size=500, overlap=100):
    if overlap >= chunk_size:
        raise ValueError("overlap doit être inférieur à chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def create_chunks(article, chunk_size=500, overlap=100):
    text_chunks = split_text(
        article["text"],
        chunk_size,
        overlap
    )

    return [
        {
            "chunk_id": f"{article['id']}_{i}",
            "article_id": article["id"],
            "title": article["title"],
            "url": article["url"],
            "chunk_index": i,
            "text": chunk
        }
        for i, chunk in enumerate(text_chunks)
    ]

def main():
    input_path = WIKIPEDIA_PATH
    output_path = CHUNKS_PATH

    all_chunks = []

    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            article = json.loads(line)
            all_chunks.extend(create_chunks(article))

    with output_path.open("w", encoding="utf-8") as file:
        for chunk in all_chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Articles traités : 101")
    print(f"Chunks créés : {len(all_chunks)}")
    print(f"Fichier enregistré : {output_path}")


if __name__ == "__main__":
    main()
