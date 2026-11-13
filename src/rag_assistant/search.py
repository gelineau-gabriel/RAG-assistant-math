import numpy as np

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

def retrieve_chunks(question, chunks, embeddings, model, top_k=5):
    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    scores = embeddings @ question_embedding

    best_indices = np.argsort(scores)[::-1][:top_k]

    context_indices = expand_context(chunks, best_indices)

    return [
        chunks[index]
        for index in context_indices
    ]

def build_context(retrieved_chunks):
    context_parts = []

    for chunk in retrieved_chunks:
        part = f"""
        Source : {chunk['title']}
        URL : {chunk['url']}

        {chunk['text']}
        """
        context_parts.append(part)

    return "\n---\n".join(context_parts)