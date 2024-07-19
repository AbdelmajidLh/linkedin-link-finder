import logging
from datetime import datetime
import os

def configure_logging():
    if not os.path.exists('log'):
        os.makedirs('log')
        
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = f"log/output_{date_str}.log"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(filename=log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)
