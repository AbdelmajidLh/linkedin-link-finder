import logging
from scripts import excel_checker
from scripts import url_finder
import pandas as pd

def chunk_dataframe(df, chunk_size):
    chunks = []
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunks.append(df[start:end])
    return chunks

def main():
    config_file_path = "conf/config.json"  # Chemin vers votre fichier de configuration
    #chunk_size = 10  # Taille des chunks pour le découpage du DataFrame

    try:
        config_data = excel_checker.load_config(config_file_path)
        excel_file_path = config_data.get("excel_file_path")
        if excel_file_path:
            # Appel de la fonction pour vérifier les colonnes Excel et obtenir les données sous forme de DataFrame
            data = excel_checker.check_excel_columns(excel_file_path)
            
            # Vérifier si les colonnes LinkedIn sont présentes dans les données
            if 'LinkedIn' not in data.columns:
                data['LinkedIn'] = None  # Si les colonnes LinkedIn ne sont pas présentes, les initialiser avec None
            
            # Diviser le DataFrame en petits sous-DataFrames
            chunk_size = config_data.get("chunk_size")
            chunks = chunk_dataframe(data, chunk_size)
            
            # Appliquer la fonction sur chaque sous-DataFrame et concaténer les résultats
            result_frames = []
            for chunk in chunks:
                result_frames.append(url_finder.generate_linkedin_urls(chunk))
            df_with_links = pd.concat(result_frames)
            
            # Afficher le DataFrame avec les liens LinkedIn
            print(df_with_links)
            
            # Enregistrer le DataFrame avec les liens LinkedIn dans un fichier Excel
            output_file_path = config_data.get("output_file_path")
            df_with_links.to_excel(output_file_path, index=False)
            print(f"Les résultats ont été enregistrés dans : {output_file_path}")
        else:
            logging.error("Chemin du fichier Excel non spécifié dans le fichier de configuration.")
    except Exception as e:
        logging.exception("Une erreur est survenue :")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
