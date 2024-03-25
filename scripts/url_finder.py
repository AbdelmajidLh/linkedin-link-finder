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
        for _ in range(max_retries):
            try:
                for url in search(query, num=1, stop=1):
                    if 'linkedin.com/in' in url:
                        return url
            except HTTPError as e:
                if e.code == 429:
                    print(f"Erreur 429: Trop de requêtes. Attente avant de réessayer...")
                    time.sleep(120)  # Attendre 120 secondes avant de réessayer
                else:
                    print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                    break  # Arrêter le traitement en cas d'autres erreurs HTTP
            except Exception as e:
                print(f"Erreur lors de la recherche de l'URL LinkedIn pour {nom}: {e}")
                print("Réessai dans quelques secondes...")
                time.sleep(5)  # Attendre quelques secondes avant de réessayer
    return None

# Appliquer la fonction sur chaque sous-DataFrame et concaténer les résultats
def generate_linkedin_urls(data, chunk_size=10):
    if isinstance(data, pd.DataFrame):
        data = data.copy()  # Copie des données pour éviter de modifier les données d'origine
        
        # Découper le DataFrame en sous-DataFrames
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Liste pour stocker les résultats de chaque sous-DataFrame
        results = []
        
        # Appliquer la fonction sur chaque sous-DataFrame
        for chunk in chunks:
            chunk['LinkedIn'] = chunk.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
            results.append(chunk)
        
        # Concaténer les résultats en un seul DataFrame
        result_df = pd.concat(results, ignore_index=True)
        
        return result_df
    else:
        raise ValueError("Les données doivent être un DataFrame.")
