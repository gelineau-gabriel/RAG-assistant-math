import json
import numpy as np
import requests

from pathlib import Path
from sentence_transformers import SentenceTransformer

from .search import retrieve_chunks, build_context

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:8b"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def load_rag():
    """Charge les données et le modèle nécessaires au RAG."""

    # Chargement des chunks
    chunks = []

    with Path("data/math_chunks.jsonl").open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    # Chargement des embeddings
    embeddings = np.load("data/math_embeddings.npy")

    # Chargement du modèle d'embeddings
    model = SentenceTransformer(EMBEDDING_MODEL)

    return chunks, embeddings, model


def answer_question(question, chunks, embeddings, model):
    """Recherche le contexte pertinent et génère une réponse."""

    # Recherche des passages pertinents
    retrieved_chunks = retrieve_chunks(
        question, chunks, embeddings, model
    )

    # Construction du contexte
    context = build_context(retrieved_chunks)

    # Construction du prompt
    prompt = f"""
Voici les extraits de documents à utiliser pour répondre à la question.

CONTEXTE :
{context}

QUESTION :
{question}

Réponds en t'appuyant prioritairement sur le contexte.
Si le contexte ne permet pas de répondre, indique-le clairement.
"""

    # Appel à Ollama
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=600
    )
    response.raise_for_status()

    return response.json()["message"]["content"]
