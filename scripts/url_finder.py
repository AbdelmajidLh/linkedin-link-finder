import pandas as pd
from googlesearch import search
import time
from urllib.error import HTTPError

# Requetes de recherche sur Google
def find_linkedin_url(nom, fonction, plateforme_ou_pole, entreprise, max_retries=3):
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
                # Remplacez 'search' par votre méthode de recherche d'URL.
                for url in search(query, num=1, stop=1):
                    if 'linkedin.com/in' in url:
                        return url
            except HTTPError as e:
                if e.code == 429:
                    wait = 2 ** attempt  # Délai exponentiel
                    print(f"Erreur 429: Trop de requêtes. Attente de {wait} secondes avant de réessayer...")
                    time.sleep(wait)
                    attempt += 1
                else:
                    print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                    break
            except Exception as e:
                print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                attempt += 1
                if attempt < max_retries:
                    print("Réessai dans quelques secondes...")
                    time.sleep(5)
    return None


# Appliquer la fonction sur chaque sous-DataFrame et concaténer les résultats
def generate_linkedin_urls(data):
    if isinstance(data, pd.DataFrame):
        data = data.copy()  # Copie des données pour éviter de modifier les données d'origine
        data['LinkedIn'] = data.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
        return data
    else:
        raise ValueError("Les données doivent être un DataFrame.")
