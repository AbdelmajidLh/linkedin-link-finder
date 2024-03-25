import logging
from googlesearch import search
import time
from urllib.error import HTTPError
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour trouver l'URL LinkedIn avec gestion des erreurs 429
def find_linkedin_url(nom, fonction, plateforme_ou_pole, entreprise, max_retries=3):
    logging.info(f"Recherche de l'URL LinkedIn pour {nom}.")
    queries = [
        f"{nom} {fonction} {plateforme_ou_pole} {entreprise} LinkedIn",
        f"{nom} {plateforme_ou_pole} {entreprise} LinkedIn",
        f"{nom} {entreprise} LinkedIn",
        f"{nom} LinkedIn"
    ]
    for query in queries:
        attempt = 0
        while attempt < max_retries:
            try:
                for url in search(query, num=1, stop=1):
                    if 'linkedin.com/in' in url:
                        logging.info(f"URL LinkedIn trouvée pour {nom}.")
                        return url
            except HTTPError as e:
                if e.code == 429:
                    wait = 2 ** attempt  # Délai exponentiel
                    logging.warning(f"Erreur 429: Trop de requêtes pour {nom}. Attente de {wait} secondes avant de réessayer...")
                    time.sleep(wait)
                    attempt += 1
                else:
                    logging.error(f"Erreur HTTP autre que 429 pour {nom}: {e}")
                    break
            except Exception as e:
                logging.error(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                attempt += 1
                if attempt < max_retries:
                    logging.info("Réessai dans quelques secondes...")
                    time.sleep(5)
    logging.info(f"Aucune URL LinkedIn trouvée pour {nom}.")
    return None

# Fonction pour générer les URLs LinkedIn pour un DataFrame
def generate_linkedin_urls(data):
    logging.info("Génération des URLs LinkedIn pour le DataFrame.")
    if isinstance(data, pd.DataFrame):
        data['LinkedIn'] = data.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
        logging.info("URLs LinkedIn générées avec succès.")
        return data
    else:
        logging.error("Les données fournies ne sont pas un DataFrame.")
        raise ValueError("Les données doivent être un DataFrame.")
