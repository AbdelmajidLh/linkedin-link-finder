import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

load_dotenv()

import logging
import time
import pandas as pd
from scripts.excel_checker import ExcelChecker
from scripts.url_finder import URLFinder
from scripts.gpt_excel_generator import GPTExcelGenerator
from scripts.pdf_extractor import PDFExtractor
from utils.api_utils import load_api_key, configure_openai
from utils.logging_utils import configure_logging

def main():
    configure_logging()
    start_time = time.time()  # Start the timer
    logging.info("Starting PDF and Excel file processing.")

    # Configuration
    config_file_path = "conf/config.json"
    excel_checker = ExcelChecker()
    
    try:
        config_data = excel_checker.load_config(config_file_path)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.error("ERROR - OpenAI API key not found in environment variables.")
            return

        configure_openai(api_key)

        excel_file_path = config_data.get("excel_file_path")
        output_file_path = config_data.get("output_file_path")
        pdf_path = config_data.get("pdf_path")
        prompt_template_path = config_data.get("prompt_template_path")
        ignore_gpt_if_excel_exists = config_data.get("ignore_gpt_if_excel_exists", False)
        nrow = config_data.get("nrow")
        time_sleep = config_data.get("time_sleep")

        # Vérifier si le fichier Excel existe et si nous devons ignorer la partie GPT
        if ignore_gpt_if_excel_exists and os.path.exists(excel_file_path):
            logging.info(f"Excel file found at {excel_file_path}. Skipping GPT processing.")
        else:
            # Extraction de texte du PDF et conversion en DataFrame
            if pdf_path:
                logging.info("Starting text extraction from PDF.")
                pdf_extractor = PDFExtractor(pdf_path)
                text_list = pdf_extractor.extract_text_from_pdf()
                logging.info("Text extracted from PDF.")

                df = pdf_extractor.pdf_to_dataframe()
                input_gpt_path = 'res/input_gpt.txt'
                df.to_csv(input_gpt_path, header=None, index=None, sep=' ', mode='a')
                logging.info("Text saved to DataFrame.")

                # Get company name from PDF file name
                company_name = os.path.basename(pdf_path).split('.')[0]
                prompt_path = f"prompts/prompt_{company_name}.txt"

                with open(prompt_template_path, 'r') as template_file:
                    prompt_template = template_file.read().strip()
                
                with open(input_gpt_path, 'r') as input_gpt_file:
                    input_gpt_text = input_gpt_file.read().strip()

                combined_prompt = f"{prompt_template}\n\n{input_gpt_text}"

                with open(prompt_path, 'w') as prompt_file:
                    prompt_file.write(combined_prompt)
                
                logging.info(f"Prompt file created: {prompt_path}")

                gpt_generator = GPTExcelGenerator(prompt_template_path)
                reponse = gpt_generator.obtenir_reponse_chatgpt(combined_prompt)
                gpt_generator.sauvegarder_dans_excel(reponse, output_file_path)
                logging.info("Response saved to Excel.")

            else:
                logging.error("ERROR - PDF file path not specified in config.")

        # Traitement du fichier Excel
        if excel_file_path:
            logging.info("Starting Excel file processing.")
            data = excel_checker.check_excel_columns(excel_file_path)

            # Découper le DataFrame en chunks de n lignes
            chunks = [data.iloc[i:i + nrow] for i in range(0, data.shape[0], nrow)]

            # Initialiser le DataFrame pour les résultats
            df_with_links = pd.DataFrame()

            # Traiter chaque chunk
            url_finder = URLFinder(config_data)
            for chunk in chunks:
                updated_chunk = url_finder.generate_linkedin_urls(chunk)
                df_with_links = pd.concat([df_with_links, updated_chunk], ignore_index=True)

                # Attendre le temps spécifié entre chaque chunk
                time.sleep(time_sleep)

            # Afficher le DataFrame avec les liens LinkedIn
            logging.info(df_with_links)

            # Enregistrer le DataFrame avec les liens LinkedIn dans un fichier Excel
            df_with_links.to_excel(output_file_path, index=False)
            logging.info(f"Results saved to: {output_file_path}")
        else:
            logging.error("ERROR - Excel file path not specified in config.")

    except Exception as e:
        logging.exception("An error occurred:")

    end_time = time.time()  # Stop the timer
    execution_time = end_time - start_time  # Calculate execution time
    logging.info(f"Program execution time: {execution_time / 60} minutes.")

if __name__ == "__main__":
    main()
