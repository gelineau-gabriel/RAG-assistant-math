from .config import DATA_DIR
from . import import_wikipedia
from . import chunking
from . import embed


def initialize_data():
    """Crée le dossier de données s'il n'existe pas."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def prepare_corpus():
    """Exécute les étapes de préparation du corpus."""
    initialize_data()

    print("1/3 - Importation des articles Wikipédia...")
    import_wikipedia.main()

    print("2/3 - Découpage des articles en chunks...")
    chunking.main()

    print("3/3 - Génération des embeddings...")
    embed.main()

    print("Préparation du corpus terminée !")


if __name__ == "__main__":
    prepare_corpus()