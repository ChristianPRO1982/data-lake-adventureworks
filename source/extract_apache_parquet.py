import pandas as pd
import numpy as np
import os
from datetime import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv
from PIL import Image
import io
import dotenv
from source.logs import init_log, logging_msg



####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    log_prefix = '[ext-apache_parquet | init]'
    try:
        dotenv.load_dotenv('.env', override=True)
        init_log()

        logging_msg(f"{log_prefix} OK")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False


####################################################################################################
####################################################################################################
####################################################################################################

def save_image(image, file_path)->bool:
    log_prefix = '[ext-apache_parquet | save_image]'
    try:
        logging_msg(f"{log_prefix} START", 'DEBUG')

        webp_file_path = f"{file_path}.webp"
        with open(webp_file_path, 'wb') as f:
            f.write(image)

        image = Image.open(webp_file_path)
        png_file_path = f"{file_path}.png"
        image.save(png_file_path, "PNG")

        os.remove(webp_file_path)

        return True

    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return False


def extract_all_png(parkets_folder, image_folder):
    log_prefix = '[ext-apache_parquet | save_image]'
    try:
        logging_msg(f"{log_prefix} START")

        DEBUG = os.getenv("DEBUG")

        os.makedirs(f"{image_folder}png/", exist_ok=True)

        for file in os.listdir(image_folder):
            if file.endswith('.csv'):
                os.remove(os.path.join(image_folder, file))

        parkets = {}
        for file in os.listdir(parkets_folder):
            if file.endswith('.parquet'):
                df = pd.read_parquet(parkets_folder + file)
                parkets[file] = int(df.image.count())

        for i, parket in enumerate(parkets):
            print('')
            print(i + 1, "sur", len(parkets), ":", parket)

            df = pd.read_parquet(parkets_folder + parket)
            
            columns = list(df.columns)
            columns.remove('image')
            
            metadata_csv_path = os.path.join(image_folder, f"{i}-metadata.csv")
            write_header = not os.path.exists(metadata_csv_path)
            with open(metadata_csv_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                if write_header:
                    writer.writeheader()
                
                for row_idx in tqdm(range(parkets[parket]), desc="genPNG"):
                    metadata = df.iloc[row_idx].drop("image").to_dict()
                    writer.writerow(metadata)

                    item_id = df.iloc[row_idx].item_ID
                    webp_bytes = df.iloc[row_idx].image
                    save_image(webp_bytes['bytes'], f"{image_folder}png/{item_id}")
                    
                    if DEBUG == '1' and row_idx > 1:
                        logging_msg(f"DEBUG MODE: {row_idx} lignes traitées", 'INFO')
                        break

    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')


####################################################################################################
####################################################################################################
####################################################################################################

############
### MAIN ###
############
def main()->bool:
    log_prefix = '[ext-apache_parquet | main]'
    try:
        if init():
            logging_msg(f"{log_prefix} START at {datetime.now()}", 'WARNING')

            parkets_folder = os.getenv("PARKETS_FOLDER")
            image_folder = os.getenv("IMAGE_FOLDER")
            print(parkets_folder, image_folder)
            extract_all_png(parkets_folder, image_folder)
            logging_msg(f"{log_prefix} ALL OK", 'WARNING')

        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False
