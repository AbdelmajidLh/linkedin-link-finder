import logging
from scripts import excel_checker, url_finder
from utils import chunks
import pandas as pd
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            # vérifier les colonnes Excel et obtenir les données sous forme de DataFrame
            data = excel_checker.check_excel_columns(excel_file_path)
            
            # Vérifier si les colonnes LinkedIn sont présentes dans les données
            if 'LinkedIn' not in data.columns:
                data['LinkedIn'] = None  # Si les colonnes LinkedIn ne sont pas présentes, les initialiser avec None
            
            # Ajouter les liens LinkedIn
            df_with_links = url_finder.generate_linkedin_urls(data)
            
            # Afficher le DataFrame avec les liens LinkedIn
            print(df_with_links)
            
            # Enregistrer le DataFrame avec les liens LinkedIn dans un fichier Excel
            #output_file_path = "linkedin_links.xlsx"  # Chemin vers le fichier de sortie
            df_with_links.to_excel(output_file_path, index=False)
            print(f"Les résultats ont été enregistrés dans : {output_file_path}")
        else:
            logging.error("Chemin du fichier Excel non spécifié dans le fichier de configuration.")
    except Exception as e:
        logging.exception("Une erreur est survenue :")
    end_time = time.time()  # Arrêter le chronomètre
    execution_time = end_time - start_time  # Calculer le temps d'exécution
    logging.info(f"Temps d'exécution du programme : {execution_time/60} minutes.")

if __name__ == "__main__":
    main()
