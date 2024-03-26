import logging
from scripts import excel_checker, url_finder
import pandas as pd
import time

# Configuration du système de logging
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
            # Vérifier les colonnes Excel et obtenir les données sous forme de DataFrame
            data = excel_checker.check_excel_columns(excel_file_path)

            # Découper le DataFrame en chunks de 10 lignes
            chunks = [data.iloc[i:i + 10] for i in range(0, data.shape[0], 10)]

            # Initialiser le DataFrame pour les résultats
            df_with_links = pd.DataFrame()

            # Traiter chaque chunk
            for chunk in chunks:
                updated_chunk = url_finder.generate_linkedin_urls(chunk)
                df_with_links = pd.concat([df_with_links, updated_chunk], ignore_index=True)

                # Attendre 2 minutes entre chaque chunk
                time.sleep(120)

            # Afficher le DataFrame avec les liens LinkedIn
            print(df_with_links)

            # Enregistrer le DataFrame avec les liens LinkedIn dans un fichier Excel
            df_with_links.to_excel(output_file_path, index=False)
            print(f"Les résultats ont été enregistrés dans : {output_file_path}")
        else:
            logging.error("Chemin du fichier Excel non spécifié dans le fichier de configuration.")
    except Exception as e:
        logging.exception("Une erreur est survenue :")
    end_time = time.time()  # Arrêter le chronomètre
    execution_time = end_time - start_time  # Calculer le temps d'exécution
    logging.info(f"Temps d'exécution du programme : {execution_time / 60} minutes.")

if __name__ == "__main__":
    main()
