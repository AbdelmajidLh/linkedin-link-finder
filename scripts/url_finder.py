import pandas as pd
import requests
import time
import logging

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
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                }
                url = 'https://www.google.com/search?q=' + query
                res = requests.get(url, headers=headers)
                res.raise_for_status()  # Raise an exception for HTTP errors
                links = res.text.split('"')
                for link in links:
                    if 'linkedin.com/in' in link:
                        return link
            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"Erreur 429: Trop de requêtes. Attente avant de réessayer...")
                    time.sleep(60)  # Attendre 60 secondes avant de réessayer
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

def generate_linkedin_urls(data):
    logging.info("Génération des URLs LinkedIn pour le DataFrame.")
    if isinstance(data, pd.DataFrame):
        data['LinkedIn'] = data.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
        logging.info("URLs LinkedIn générées avec succès.")
        return data
    else:
        logging.error("Les données fournies ne sont pas un DataFrame.")
        raise ValueError("Les données doivent être un DataFrame.")
