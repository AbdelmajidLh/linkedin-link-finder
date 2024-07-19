import openai
import logging

def load_api_key(api_key_path):
    try:
        with open(api_key_path, 'r') as file:
            api_key = file.read().strip()
        logging.info("API key loaded successfully.")
        return api_key
    except Exception as e:
        logging.error(f"Error loading API key: {e}")
        raise

def configure_openai(api_key):
    openai.api_key = api_key
    logging.info("OpenAI API configured successfully.")
