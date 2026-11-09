import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

def expand_context(chunks, best_indices):
    # Index rapide : (article_id, chunk_index) -> position dans chunks
    chunk_lookup = {
        (chunk["article_id"], chunk["chunk_index"]): i
        for i, chunk in enumerate(chunks)
    }

    context_indices = set()

    for index in best_indices:
        chunk = chunks[index]
        article_id = chunk["article_id"]
        chunk_index = chunk["chunk_index"]

        # Ajouter le chunk précédent, le chunk courant et le suivant
        for offset in (-1, 0, 1):
            key = (article_id, chunk_index + offset)

            if key in chunk_lookup:
                context_indices.add(chunk_lookup[key])

    return sorted(
        context_indices,
        key=lambda i: (
            str(chunks[i]["article_id"]),
            chunks[i]["chunk_index"]
        )
    )

def main():
    # Charger les chunks
    chunks = []
    with Path("data/math_chunks.jsonl").open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    # Charger les embeddings
    embeddings = np.load("data/math_embeddings.npy")

    # Charger le modèle
    model = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Question de l'utilisateur
    question = "Quelle est la différence entre un groupe et un corps ?"

    # Transformer la question en vecteur
    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    # Calculer les similarités
    scores = embeddings @ question_embedding

    # Récupérer les 3 meilleurs résultats
    top_k = 10
    best_indices = np.argsort(scores)[::-1][:top_k]

    context_indices = expand_context(chunks, best_indices)
    best_set = set(best_indices)

    print(f"\nMeilleurs résultats : {top_k}")
    print(f"Chunks affichés avec contexte : {len(context_indices)}")

    for index in context_indices:
        chunk = chunks[index]

        if index in best_set:
            status = "RÉSULTAT"
        else:
            status = "CONTEXTE"

        print("\n" + "=" * 60)
        print(f"[{status}]")
        print(f"Titre : {chunk['title']}")
        print(f"Chunk : {chunk['chunk_id']}")

        if index in best_set:
            print(f"Score : {scores[index]:.4f}")

        print(chunk["text"])

if __name__ == "__main__":
    main()