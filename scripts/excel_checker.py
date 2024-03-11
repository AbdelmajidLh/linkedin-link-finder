import logging
import pandas as pd
import os
import json

# Configuration du système de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# load config
def load_config(config_file_path):
    try:
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier de configuration : {e}")
        raise

# load and check axcel file
def check_excel_columns(excel_file_path):
    # Vérifier si le fichier Excel existe
    if not os.path.exists(excel_file_path):
        logging.error(f"Le fichier Excel {excel_file_path} n'existe pas.")
        raise FileNotFoundError(f"Le fichier Excel {excel_file_path} n'existe pas.")

    # Lire le fichier Excel
    try:
        df = pd.read_excel(excel_file_path)
        logging.info("Les premières lignes du DataFrame :")
        logging.info(df.head())

    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier Excel : {e}")
        raise

    # Vérifier si les colonnes nécessaires existent
    required_columns = ["Nom", "Fonction", "Plateforme ou pôle", "Entreprise", "LinkedIn"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"Les colonnes suivantes sont manquantes dans le fichier Excel : {', '.join(missing_columns)}")
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le fichier Excel : {', '.join(missing_columns)}")
    
    logging.info("Toutes les colonnes requises sont présentes dans le fichier Excel.")

#if __name__ == "__main__":
#    excel_file_path = "data/file.xlsx"  # Chemin vers votre fichier Excel
#
#    try:
#        check_excel_columns(excel_file_path)
#    except Exception as e:
#        logging.exception("Une erreur est survenue :")
