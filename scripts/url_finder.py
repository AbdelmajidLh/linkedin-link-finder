import pandas as pd
from googlesearch import search

def find_linkedin_url(nom, fonction, plateforme_ou_pole, entreprise):
    queries = [
        f"{nom} {fonction} {plateforme_ou_pole} {entreprise} LinkedIn",
        f"{nom} {plateforme_ou_pole} {entreprise} LinkedIn",
        f"{nom} {entreprise} LinkedIn",
        f"{nom} LinkedIn"
    ]
    for query in queries:
        for url in search(query, num=1, stop=1):
            if 'linkedin.com/in' in url:
                return url
    return None

def generate_linkedin_urls(data):
    if isinstance(data, pd.DataFrame):
        data = data.copy()  # Copie des données pour éviter de modifier les données d'origine
        data['LinkedIn'] = data.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
        return data
    else:
        raise ValueError("Les données doivent être un DataFrame.")
