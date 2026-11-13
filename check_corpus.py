import json
import statistics
from pathlib import Path
from collections import Counter

CORPUS_PATH = Path("data/wikipedia_math.jsonl")
MIN_LENGTH = 200  # seuil indicatif en caractères


def load_articles():
    articles = []

    with CORPUS_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                articles.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"ERREUR JSON à la ligne {line_number}")

    return articles


def check_corpus():
    articles = load_articles()

    print("\n========== BILAN DU CORPUS ==========\n")

    # 1. Nombre d'articles
    print(f"Nombre d'articles : {len(articles)}")
    if len(articles) == 101:
        print("OK : nombre attendu.")
    else:
        print("ATTENTION : nombre différent de 20.")

    # 2. Titres et doublons
    titles = [a.get("title", "") for a in articles]
    duplicates = [
        title for title, count in Counter(titles).items()
        if count > 1
    ]

    print(f"\nTitres uniques : {len(set(titles))}")
    print(f"Doublons : {duplicates if duplicates else 'Aucun'}")

    # 3. Textes vides ou courts
    empty = [a["title"] for a in articles if not a.get("text", "").strip()]
    short = [
        (a["title"], len(a.get("text", "")))
        for a in articles
        if 0 < len(a.get("text", "").strip()) < MIN_LENGTH
    ]

    print(f"\nTextes vides : {empty if empty else 'Aucun'}")
    print(f"Textes courts (< {MIN_LENGTH} caractères) :")
    print(short if short else "Aucun")

    # 4. Longueur des articles
    lengths = [len(a.get("text", "")) for a in articles]

    if lengths:
        print("\nLongueur des articles (caractères) :")
        print(f"Minimum : {min(lengths)}")
        print(f"Maximum : {max(lengths)}")
        print(f"Moyenne : {statistics.mean(lengths):.0f}")
        print(f"Médiane : {statistics.median(lengths):.0f}")
        print(f"Total : {sum(lengths):,}")

    # 5. Caractères de contrôle
    control_chars = []
    for article in articles:
        for char in article.get("text", ""):
            if ord(char) < 32 and char not in "\n\r\t":
                control_chars.append((article["title"], repr(char)))

    print("\nCaractères de contrôle inattendus :")
    print(control_chars[:20] if control_chars else "Aucun")

    # 6. Pages de navigation
    navigation = [
        a["title"] for a in articles
        if a.get("title", "").startswith(
            ("Portail:", "Catégorie:", "Wikipédia:")
        )
    ]

    print("\nPages de navigation ou catégories :")
    print(navigation if navigation else "Aucune")

    # Vérification des champs et URLs
    print("\nChamps manquants :")
    required = ("id", "title", "text", "url")
    missing = [
        a.get("title", f"Article {i}")
        for i, a in enumerate(articles)
        if any(not a.get(field) for field in required)
    ]
    print(missing if missing else "Aucun")

    print("\n========== FIN DES CONTRÔLES ==========\n")


if __name__ == "__main__":
    check_corpus()
