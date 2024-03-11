import logging
from scripts import excel_checker
from scripts import url_finder

def main():
    config_file_path = "conf/config.json"  # Chemin vers votre fichier de configuration

    try:
        config_data = excel_checker.load_config(config_file_path)
        excel_file_path = config_data.get("excel_file_path")
        if excel_file_path:
            data = excel_checker.check_excel_columns(excel_file_path)
            #df_with_links = url_finder.generate_linkedin_urls(data)  # Appel de la fonction pour ajouter les liens LinkedIn
            #print(df_with_links)  # Afficher le DataFrame avec les liens LinkedIn
            print(data)
        else:
            logging.error("Chemin du fichier Excel non spécifié dans le fichier de configuration.")
    except Exception as e:
        logging.exception("Une erreur est survenue :")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
