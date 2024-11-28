import os
import shutil
import dotenv
from source.logs import init_log, logging_msg



####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    log_prefix = '[ext-CSV_compressed | init]'
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

def extract_compressed_file(zip_file:str, output_folder:str)->bool:
    log_prefix = '[ext-CSV_compressed | extract_compressed_file]'
    try:
        logging_msg(f"{log_prefix} START: {zip_file}")

        shutil.unpack_archive(zip_file, output_folder)
        
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        logging_msg(f"{log_prefix} Zip file on error: {zip_file}", 'ERROR')
        return False

def scan_folder(input_folder:str, output_folder:str, unextracted_zip_folder:str, removed: bool)->bool:
    log_prefix = '[ext-CSV_compressed | scan_folder]'
    try:
        logging_msg(f"{log_prefix} START")

        DEBUG = os.getenv('DEBUG')

        os.makedirs(output_folder, exist_ok=True)

        # scan zip files in the input folder
        recursive = False
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if unextracted_zip_folder in file:
                    continue
                if file.endswith(('.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar.xz', '.txz')):
                    recursive = True
                    if DEBUG == '1':
                        logging_msg(f"{log_prefix} Extracting: {file}", 'DEBUG')
                        
                    if extract_compressed_file(os.path.join(root, file), output_folder):
                        if removed:
                            os.remove(os.path.join(root, file))
                    else:
                        if removed:
                            os.makedirs(unextracted_zip_folder, exist_ok=True)
                            os.rename(os.path.join(root, file), os.path.join(unextracted_zip_folder, file))
                else:
                    if DEBUG == '1':
                        logging_msg(f"{log_prefix} Not a zip file: {file}", 'DEBUG')
        
        # recusively scan the extracted folder
        if recursive:
            if DEBUG == '1':
                logging_msg(f"{log_prefix} Recursive scan", 'DEBUG')    
            scan_folder(output_folder, output_folder, unextracted_zip_folder, True) 
        

        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return False


####################################################################################################
####################################################################################################
####################################################################################################

############
### MAIN ###
############
def main()->bool:
    log_prefix = '[ext-CSV_compressed | main]'
    try:
        if init():
            ZIP_FOLDER = os.getenv('ZIP_FOLDER')
            EXTRACTED_FOLDER = os.getenv('EXTRACTED_FOLDER')
            UNEXTRACTED_FOLDER = os.getenv('UNEXTRACTED_FOLDER')

            scan_folder(ZIP_FOLDER, EXTRACTED_FOLDER, UNEXTRACTED_FOLDER, False)

            logging_msg(f"{log_prefix} ALL OK")

        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False
