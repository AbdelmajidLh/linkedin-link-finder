import logging
import pandas as pd
import os
import json

class ExcelChecker:
    def load_config(self, config_file_path):
        logging.info(f"Loading config file: {config_file_path}")
        try:
            with open(config_file_path, 'r') as config_file:
                config_data = json.load(config_file)
                logging.info("Config file loaded successfully.")
                return config_data
        except Exception as e:
            logging.error(f"Error reading config file: {e}")
            raise

    def check_excel_columns(self, excel_file_path):
        logging.info(f"Checking Excel file: {excel_file_path}")
        if not os.path.exists(excel_file_path):
            logging.error(f"Excel file {excel_file_path} does not exist.")
            raise FileNotFoundError(f"Excel file {excel_file_path} does not exist.")

        try:
            df = pd.read_excel(excel_file_path)
            logging.info("Excel file read successfully.")
        except Exception as e:
            logging.error(f"Error reading Excel file: {e}")
            raise

        required_columns = ["Nom", "Fonction", "Plateforme ou pôle", "Entreprise", "LinkedIn"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            logging.error(f"Missing columns in Excel file: {', '.join(missing_columns)}")
            raise ValueError(f"Missing columns in Excel file: {', '.join(missing_columns)}")

        logging.info("All required columns are present in the Excel file.")
        return df
