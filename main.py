import logging
from scripts import excel_checker
from scripts import url_finder
import pandas as pd

def main():
    config_file_path = "conf/config.json"  # Chemin vers votre fichier de configuration

    try:
        config_data = excel_checker.load_config(config_file_path)
        excel_file_path = config_data.get("excel_file_path")
        if excel_file_path:
            # Appel de la fonction pour vérifier les colonnes Excel et obtenir les données sous forme de DataFrame
            data = excel_checker.check_excel_columns(excel_file_path)
            
            # Vérifier si les colonnes LinkedIn sont présentes dans les données
            if 'LinkedIn' not in data.columns:
                data['LinkedIn'] = None  # Si les colonnes LinkedIn ne sont pas présentes, les initialiser avec None
            
            # Appel de la fonction pour ajouter les liens LinkedIn
            df_with_links = url_finder.generate_linkedin_urls(data)
            
            # Afficher le DataFrame avec les liens LinkedIn
            print(df_with_links)
            
            # Enregistrer le DataFrame avec les liens LinkedIn dans un fichier Excel
            output_file_path = "res/output.xlsx"  # Chemin vers le fichier de sortie
            df_with_links.to_excel(output_file_path, index=False)
            print(f"Les résultats ont été enregistrés dans : {output_file_path}")
        else:
            logging.error("Chemin du fichier Excel non spécifié dans le fichier de configuration.")
    except Exception as e:
        logging.exception("Une erreur est survenue :")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
