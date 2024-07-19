import pandas as pd
import requests
import time
import logging

class URLFinder:
    def __init__(self, config):
        self.config = config

    def find_linkedin_url(self, nom, fonction, plateforme_ou_pole, entreprise, max_retries=3):
        logging.info(f"Searching LinkedIn URL for {nom}.")
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
                    res.raise_for_status()
                    links = res.text.split('"')
                    for link in links:
                        if 'linkedin.com/in' in link:
                            return link
                except requests.HTTPError as e:
                    if e.response.status_code == 429:
                        logging.warning(f"HTTP 429: Too many requests. Waiting before retrying...")
                        time.sleep(60)
                    else:
                        logging.error(f"HTTP error {e.response.status_code} for {nom}: {e}")
                        break
                except Exception as e:
                    logging.error(f"Error searching LinkedIn URL for {nom}: {e}")
                    attempt += 1
                    if attempt < max_retries:
                        logging.info("Retrying in a few seconds...")
                        time.sleep(5)
        logging.info(f"No LinkedIn URL found for {nom}.")
        return None

    def generate_linkedin_urls(self, data):
        logging.info("Generating LinkedIn URLs for DataFrame.")
        if isinstance(data, pd.DataFrame):
            data['LinkedIn'] = data.apply(lambda row: self.find_linkedin_url(row['Nom'], row['Fonction'], row['Plateforme ou pôle'], row['Entreprise']), axis=1)
            logging.info("LinkedIn URLs generated successfully.")
            return data
        else:
            logging.error("Input data is not a DataFrame.")
            raise ValueError("Data must be a DataFrame.")
