import pandas as pd
from googlesearch import search
import time
from urllib.error import HTTPError

def find_linkedin_url(nom, fonction, plateforme_ou_pole, entreprise, max_retries=3):
    queries = [
        f"{nom} {fonction} {plateforme_ou_pole} {entreprise} LinkedIn",
        f"{nom} {plateforme_ou_pole} {entreprise} LinkedIn",
        f"{nom} {entreprise} LinkedIn",
        f"{nom} LinkedIn"
    ]
    for query in queries:
        for _ in range(max_retries):
            try:
                for url in search(query, num=1, stop=1):
                    if 'linkedin.com/in' in url:
                        return url
            except HTTPError as e:
                if e.code == 429:
                    print(f"Erreur 429: Trop de requêtes. Attente avant de réessayer...")
                    time.sleep(60)  # Attendre 60 secondes avant de réessayer
                else:
                    print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                    break  # Arrêter le traitement en cas d'autres erreurs HTTP
            except Exception as e:
                print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                print("Réessai dans quelques secondes...")
                time.sleep(5)  # Attendre quelques secondes avant de réessayer
    return None

def generate_linkedin_urls(data_chunk):
    data_chunk['LinkedIn'] = data_chunk.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
    return data_chunk
