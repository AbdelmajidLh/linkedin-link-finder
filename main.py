import logging
from scripts import excel_checker
from scripts import url_finder
import pandas as pd
import math

# decouper le df pour avoir  moins de 10 lignes par chunk
def chunk_dataframe(df, max_lines=10):
    chunk_size = math.ceil(len(df) / math.ceil(len(df) / max_lines))
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunks.append(df[i:i + chunk_size])
    return chunks


def main():
    config_file_path = "conf/config.json"

    try:
        config_data = excel_checker.load_config(config_file_path)
        excel_file_path = config_data.get("excel_file_path")
        output_file_path = config_data.get("output_file_path")
        if excel_file_path:
            # Charger le fichier Excel et vérifier ses colonne 
            data = excel_checker.check_excel_columns(excel_file_path)
            
            # Vérifier la colonne LinkedIn dans le df
            if 'LinkedIn' not in data.columns:
                data['LinkedIn'] = None
            
            # Diviser le DataFrame en petits sous-DataFrames
            chunk_size = config_data.get("chunk_size")
            chunks = chunk_dataframe(data)
            print(f"Nombre de chunks : {len(chunks)}")
            
            # Appliquer la fonction sur chaque sous-DataFrame et concaténer les résultats
            result_frames = []
            for i, chunk in enumerate(chunks):
                 print(f"Traitement du chunk {i+1}/{len(chunks)}...")
                 result_frames.append(url_finder.generate_linkedin_urls(chunk))
                 print(f"Chunk {i+1} traité. URLs LinkedIn générées : {len(result_frames[-1])}")
            
            print("Assemblage des dataframes...")
            df_with_links = pd.concat(result_frames)

            # Afficher le DataFrame avec les liens LinkedIn
            print(f"Dimentions df with links : {df_with_links}")
            
            # Enregistrer les résultats dans un fichier Excel
            df_with_links.to_excel(output_file_path, index=False)
            print(f"Les résultats ont été enregistrés dans : {output_file_path}")
        else:
            logging.error("Chemin du fichier Excel non spécifié dans le fichier de configuration.")
    except Exception as e:
        logging.exception("Une erreur est survenue :")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
