import logging
from scripts import excel_checker, url_finder
import pandas as pd
import math
from concurrent.futures import ThreadPoolExecutor
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

# Fonction principale
def main():
    start_time = time.time()  # Démarrer le chronomètre
    logging.info("Début du traitement du fichier Excel.")
    config_file_path = "conf/config.json"
    try:
        config_data = excel_checker.load_config(config_file_path)
        excel_file_path = config_data.get("excel_file_path")
        output_file_path = config_data.get("output_file_path")
        if excel_file_path:
            data = excel_checker.check_excel_columns(excel_file_path)
            if 'LinkedIn' not in data.columns:
                data['LinkedIn'] = None  # Si les colonnes LinkedIn ne sont pas présentes, les initialiser avec None
            
            # Appel de la fonction pour ajouter les liens LinkedIn
            df_with_links = url_finder.generate_linkedin_urls(data)
            
            # Afficher le DataFrame avec les liens LinkedIn
            print(df_with_links)
            
            # Enregistrer le DataFrame avec les liens LinkedIn dans un fichier Excel
            output_file_path = "res/output.xlsx"  # Chemin vers le fichier de sortie
            df_with_links.to_excel(output_file_path, index=False)
            logging.info(f"Les résultats ont été enregistrés dans : {output_file_path}")
    except Exception as e:
        logging.exception("Une erreur est survenue :")
    end_time = time.time()  # Arrêter le chronomètre
    execution_time = end_time - start_time  # Calculer le temps d'exécution
    logging.info(f"Temps d'exécution du programme : {execution_time/60} minutes.")

if __name__ == "__main__":
    main()
