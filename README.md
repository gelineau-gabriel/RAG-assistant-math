# Assistant RAG mathématique avec MCP

## Présentation

Ce projet consiste à développer un assistant conversationnel capable de répondre à des questions mathématiques en s'appuyant sur un corpus documentaire spécialisé.

Il repose sur une architecture **Retrieval-Augmented Generation (RAG)**, associée au protocole **Model Context Protocol (MCP)**.

L'objectif est de combiner la recherche sémantique dans une base documentaire avec les capacités de génération d'un modèle de langage local, afin de produire des réponses contextualisées et pertinentes.

## Fonctionnalités

- Constitution d'un corpus documentaire à partir d'articles Wikipédia consacrés aux mathématiques.
- Découpage des documents en segments (*chunks*) avec chevauchement.
- Génération d'embeddings à l'aide de Sentence Transformers.
- Recherche sémantique des passages les plus pertinents.
- Extension du contexte avec les segments voisins.
- Génération de réponses à l'aide d'un modèle de langage local via Ollama.
- Exposition du moteur RAG sous forme d'outil MCP.
- Communication entre un client MCP et le serveur.

## Architecture

Le projet suit un pipeline organisé en plusieurs étapes :

1. **Collecte des données** : récupération d'articles Wikipédia consacrés à l'algèbre.
2. **Prétraitement** : découpage des articles en chunks de 500 caractères, avec un chevauchement de 100 caractères.
3. **Vectorisation** : transformation des chunks en embeddings numériques.
4. **Recherche sémantique** : comparaison entre l'embedding de la question et ceux du corpus à l'aide de la similarité cosinus.
5. **Construction du contexte** : récupération des passages pertinents et de leurs segments voisins.
6. **Génération** : transmission du contexte et de la question à Qwen3 via Ollama.
7. **Exposition MCP** : mise à disposition du moteur RAG à travers un outil appelé `ask_rag`.

### Schéma simplifié

```text
                 CORPUS DOCUMENTAIRE
                    (Wikipédia)
                         |
                         v
                  Prétraitement
                         |
                         v
                  Découpage en chunks
                         |
                         v
                 Génération embeddings
                         |
                         v
                  Base vectorielle
                         |
                         |
QUESTION ---> Client MCP ---> Serveur MCP
                                  |
                                  v
                            Outil ask_rag
                                  |
                                  v
                         Recherche sémantique
                                  |
                                  v
                         Construction contexte
                                  |
                                  v
                            Ollama / Qwen3
                                  |
                                  v
                              Réponse
```

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Développement du projet |
| Wikipédia API | Collecte documentaire |
| PyMuPDF | Extraction de texte PDF (expérimentation) |
| Sentence Transformers | Génération des embeddings |
| NumPy | Stockage et comparaison des vecteurs |
| Ollama | Exécution locale du modèle de langage |
| Qwen3 8B | Génération des réponses |
| MCP | Exposition du moteur RAG sous forme d'outil |
| Git | Gestion du code source |

## Organisation du projet

```text
rag-mcp-assistant/
│
├── documents/                 # Documents sources
│
├── data/
│   ├── extracted/             # Textes extraits
│   ├── wikipedia_math.jsonl   # Corpus documentaire
│   ├── math_chunks.jsonl      # Segments du corpus
│   └── math_embeddings.npy    # Embeddings
│
├── src/
│   └── rag_assistant/
│       ├── extract.py         # Extraction de texte
│       ├── import_wikipedia.py# Import des articles Wikipédia
│       ├── check_corpus.py    # Vérification du corpus
│       ├── chunking.py        # Découpage des documents
│       ├── embed.py           # Génération des embeddings
│       ├── search.py          # Recherche sémantique
│       ├── answer.py          # Génération des réponses
│       ├── server.py          # Serveur MCP
│       └── test_client.py     # Client de test MCP
│
├── tests/                     # Tests
├── pyproject.toml             # Configuration du projet
├── .gitignore
└── README.md
```

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd rag-mcp-assistant
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

### 4. Installer et préparer Ollama

Installer Ollama, puis télécharger le modèle utilisé :

```bash
ollama pull qwen3:8b
```

Vérifier que le modèle est disponible :

```bash
ollama list
```

Ollama doit être accessible à l'adresse :

```text
http://localhost:11434
```

## Utilisation

Le projet nécessite les fichiers du corpus, les chunks et les embeddings générés lors des étapes de préparation des données.

Une fois ces ressources disponibles et Ollama démarré, le client de test peut être exécuté depuis la racine du projet :

```bash
PYTHONPATH=src python -m rag_assistant.test_client
```

Le client initialise une session MCP, découvre les outils disponibles et appelle l'outil `ask_rag`.

### Exemple de question

```text
Quelle est la différence entre un groupe et un corps ?
```

L'assistant recherche les passages pertinents dans son corpus documentaire, construit un contexte et transmet le tout à Qwen3 pour générer une réponse.

## Perspectives d'amélioration

Plusieurs évolutions sont envisageables :

- Améliorer la qualité du découpage des documents.
- Enrichir le corpus documentaire.
- Optimiser la recherche sémantique et le classement des résultats.
- Améliorer la gestion des sources et des références dans les réponses.
- Ajouter des tests automatisés.
- Connecter le serveur à différentes applications compatibles MCP.
- Améliorer la gestion des erreurs et des délais d'exécution.

## Auteur

Projet personnel réalisé dans le cadre de l'apprentissage de Python, des architectures RAG et du protocole Model Context Protocol.