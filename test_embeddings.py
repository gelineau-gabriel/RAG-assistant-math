from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

sentences = [
    "L'algèbre est une branche des mathématiques.",
    "La géométrie étudie les formes et les espaces."
]

embeddings = model.encode(sentences, normalize_embeddings=True)

print("Dimensions :", embeddings.shape)
print("Premier vecteur :", embeddings[0][:5])