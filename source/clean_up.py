import shutil
import dotenv
import os
from source.logs import init_log, logging_msg


####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    log_prefix = '[clean_up | init]'
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

def move_files(i_folder:str, o_folder:str)->int:
    log_prefix = '[clean_up | move_files]'
    try:
        logging_msg(f"{log_prefix} Move files from {i_folder} to {o_folder}")

        DEBUG = os.getenv('DEBUG')

        os.makedirs(o_folder, exist_ok=True)

        for item in os.listdir(i_folder):
            source = os.path.join(i_folder, item)
            destination = os.path.join(o_folder, item)

            if DEBUG == '1':
                logging_msg(f"{log_prefix} Move {source} to {destination}", 'DEBUG')
            
            shutil.move(source, destination)

        return 0
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return 1


####################################################################################################
####################################################################################################
####################################################################################################

############
### MAIN ###
############
def main()->bool:
    log_prefix = '[clean_up | main]'
    try:
        if init():
            DEBUG = os.getenv('DEBUG')
            IO_FOLDERS = os.getenv('IO_FOLDERS').split(',')
            RMTREE_FOLDER = os.getenv('RMTREE_FOLDER')
            
            no_moved_folders = 0
            for io_folder in IO_FOLDERS:
                i_folder, o_folder = io_folder.split(':')
                no_moved_folders += move_files(i_folder, o_folder)

            if DEBUG != '1':
                if no_moved_folders == 0:
                    shutil.rmtree(RMTREE_FOLDER)
            else:
                logging_msg(f"{log_prefix} Remove {RMTREE_FOLDER}", 'DEBUG')

            if no_moved_folders == 0:
                logging_msg(f"{log_prefix} ALL OK", 'WARNING')
            else:    
                logging_msg(f"{log_prefix} Error: {no_moved_folders} folders not moved", 'WARNING')

        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False