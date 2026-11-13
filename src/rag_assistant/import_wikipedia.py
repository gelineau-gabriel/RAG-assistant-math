import json
import requests
import time

API_URL = "https://fr.wikipedia.org/w/api.php"
NB_ARTICLES = 101

HEADERS = {
    "User-Agent": "rag-mcp-assistant/0.1"
}

def safe_get(url, params):
    for attempt in range(5):
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=30,
        )

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 10))
            print(f"Limite Wikipédia : attente de {wait} secondes...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        time.sleep(1)
        return response

    raise RuntimeError("Wikipédia reste indisponible après 5 tentatives.")

def get_math_articles():
    categories = [
        "Algèbre",
        "Algèbre générale"
    ]

    articles = {}
    
    for category in categories:
        response = safe_get(
            API_URL,
            params={
                "action": "query",
                "list": "categorymembers",
                "cmtitle": f"Catégorie:{category}",
                "cmtype": "page",
                "cmlimit": 101,
                "format": "json",
            }
        )
        response.raise_for_status()

        members = response.json()["query"]["categorymembers"]

        for member in members:
            title = member["title"]

            if title.startswith(("Portail:", "Catégorie:", "Wikipédia:", "Utilisateur:")):
                continue

            articles[member["pageid"]] = title

    print(f"{len(articles)} articles candidats trouvés.")

    # Limiter à 100 articles
    selected = list(articles.items())[:NB_ARTICLES]
    page_ids = [page_id for page_id, _ in selected]

    if not page_ids:
        return []
    
    
    articles = []

    for page_id, title in selected:
        response = safe_get(API_URL, {
            "action": "query",
            "pageids": str(page_id),
            "prop": "extracts",
            "explaintext": True,
            "format": "json",
    })

        pages = response.json()["query"]["pages"]

        page = next(iter(pages.values()))

        article = {
        "id": page["pageid"],
        "title": page["title"],
        "text": page.get("extract", ""),
        "url": (
            "https://fr.wikipedia.org/wiki/"
            + page["title"].replace(" ", "_")
        ),
    }

        articles.append(article)

        print(f"{title} : {len(article['text'])} caractères")

    return articles

if __name__ == "__main__":
    articles = get_math_articles()

    with open("data/wikipedia_math.jsonl", "w", encoding="utf-8") as f:
        for article in articles:
            f.write(json.dumps(article, ensure_ascii=False) + "\n")

    print(f"\n{len(articles)} articles enregistrés.")

    for article in articles:
        print("-", article["title"])
