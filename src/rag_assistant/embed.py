import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from .config import EMBEDDINGS_PATH, CHUNKS_PATH

def main():
    input_path = CHUNKS_PATH
    output_path = EMBEDDINGS_PATH

    # Charger les chunks
    chunks = []

    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    print(f"Chunks chargés : {len(chunks)}")

    # Charger le modèle
    model = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Extraire les textes
    texts = [chunk["text"] for chunk in chunks]

    # Calculer les embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    # Enregistrer les vecteurs
    np.save(output_path, embeddings)

    print(f"Dimensions : {embeddings.shape}")
    print(f"Fichier enregistré : {output_path}")


if __name__ == "__main__":
    main()