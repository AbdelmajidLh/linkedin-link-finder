import pandas as pd
import requests
import time

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
                    print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                    break  # Arrêter le traitement en cas d'autres erreurs HTTP
            except Exception as e:
                print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                print("Réessai dans quelques secondes...")
                time.sleep(5)  # Attendre quelques secondes avant de réessayer
    return None

def generate_linkedin_urls(data):
    if isinstance(data, pd.DataFrame):
        data = data.copy()  # Copie des données pour éviter de modifier les données d'origine
        data['LinkedIn'] = data.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
        return data
    else:
        raise ValueError("Les données doivent être un DataFrame.")
