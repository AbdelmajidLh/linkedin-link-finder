from googlesearch import search
import pandas as pd

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
    df = pd.DataFrame(data)
    df['LinkedIn'] = df.apply(lambda row: find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
    return df
