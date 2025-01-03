import datetime
import logging
import os



def init_log()->bool:
    try:
        DEBUG = os.getenv("DEBUG")

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        os.makedirs('./logs/', exist_ok=True)
        log_filename = f"./logs/{date_str}.log"

        if DEBUG == '1':
            print("§§§§§§§§§§§§§§§§§§§§§§")
            print("§§§§§ DEBUG MODE §§§§§")
            print("§§§§§§§§§§§§§§§§§§§§§§")
            logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.getLogger("azure").setLevel(logging.INFO)
        else:
            logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.getLogger("azure").setLevel(logging.CRITICAL)
        
        return True
    
    except Exception as e:
        print(f"Error in logging.py init_log(): {e}")
        return False


def logging_msg(msg, type='INFO')->bool:
    try:
        logger = logging.getLogger(__name__)
        # print(logging.getLevelName(logger.getEffectiveLevel()))

        type = type.upper()

        if type == 'INFO':
            logger.info(msg)
        elif type == 'DEBUG':
            logger.debug(msg)
        elif type == 'ERROR':
            logger.error(msg)
        elif type == 'WARNING':
            logger.warning(msg)
        elif type == 'CRITICAL':
            logger.critical(msg)

        if type != 'DEBUG':
            print(f"[{type}] {msg} : ")

        return True

    except Exception as e:
        print(f"Error in logging.py logging_msg(): {e}")
        return False