from pathlib import Path

# Racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dossier des données
DATA_DIR = PROJECT_ROOT / "data"

# Fichiers du pipeline
WIKIPEDIA_PATH = DATA_DIR / "wikipedia_math.jsonl"
CHUNKS_PATH = DATA_DIR / "math_chunks.jsonl"
EMBEDDINGS_PATH = DATA_DIR / "math_embeddings.npy"