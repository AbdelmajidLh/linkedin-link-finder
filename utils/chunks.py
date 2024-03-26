import logging
import math
import pandas as pd
# Fonction pour découper le dataframe en chunks
def chunk_dataframe(df, max_lines=10):
    logging.info("Découpage du DataFrame en chunks.")
    chunk_size = math.ceil(len(df) / math.ceil(len(df) / max_lines))
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

# Fonction pour traiter un chunk et gérer les erreurs
def process_chunk(chunk):
    logging.info("Traitement d'un chunk du DataFrame.")
    try:
        return url_finder.generate_linkedin_urls(chunk)
    except Exception as e:
        logging.exception(f"Erreur lors du traitement du chunk : {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur