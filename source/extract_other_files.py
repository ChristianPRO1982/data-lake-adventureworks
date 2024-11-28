import os
import dotenv
from source.logs import init_log, logging_msg



####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    log_prefix = '[ext-other_files | init]'
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

def clean_folder(folder: str, extensions: list) -> None:
    log_prefix = '[ext-other_files | clean_folder]'
    try:
        logging_msg(f"{log_prefix} Cleaning folder: {folder}")

        DEBUG = os.getenv('DEBUG')

        for filename in os.listdir(folder):
            if not any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    if DEBUG == '1':
                        logging_msg(f"{log_prefix} Removed: {file_path}", 'DEBUG')

        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False


####################################################################################################
####################################################################################################
####################################################################################################

############
### MAIN ###
############
def main()->bool:
    log_prefix = '[ext-other_files | main]'
    try:
        if init():
            OTHER_FILES_FOLDER = os.getenv('OTHER_FILES_FOLDER')
            EXTENSIONS = os.getenv('EXTENSIONS').split(',')

            if clean_folder(OTHER_FILES_FOLDER, EXTENSIONS):
                logging_msg(f"{log_prefix} ALL OK")

        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False
