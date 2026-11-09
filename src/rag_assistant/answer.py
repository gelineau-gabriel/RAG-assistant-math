import json
import numpy as np
import requests

from pathlib import Path
from sentence_transformers import SentenceTransformer

from search import retrieve_chunks, build_context

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:8b"


def generate_answer(question, context=""):
    prompt = f"""
Voici les extraits de documents à utiliser pour répondre à la question.

CONTEXTE :
{context}

QUESTION :
{question}

Réponds en t'appuyant prioritairement sur le contexte.
Si le contexte ne permet pas de répondre, indique-le clairement.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["message"]["content"]


def main():
    # Chargement des chunks
    chunks = []

    with Path("data/math_chunks.jsonl").open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    # Chargement des embeddings
    embeddings = np.load("data/math_embeddings.npy")

    # Chargement du modèle d'embeddings
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    # Question utilisateur
    question = input("Pose ta question : ")

    # Recherche des passages pertinents
    retrieved_chunks = retrieve_chunks(
        question, chunks, embeddings, model
    )

    # Construction du contexte
    context = build_context(retrieved_chunks)

    # Génération de la réponse
    answer = generate_answer(question, context)

    print("\nRéponse de l'assistant :\n")
    print(answer)


if __name__ == "__main__":
    main()
