import datetime
import logging
import os



def init_log()->bool:
    try:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        os.makedirs('../logs/', exist_ok=True)
        log_filename = f"./logs/{date_str}.log"
        logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        return True
    
    except Exception as e:
        print(f"Error in logging.py init_lot(): {e}")
        return False


def logging_msg(msg, type='info')->bool:
    try:
        logger = logging.getLogger(__name__)

        if type == 'info':
            logger.info(msg)
        elif type == 'debug':
            logger.debug(msg)
        elif type == 'error':
            logger.error(msg)
        elif type == 'warning':
            logger.warning(msg)
        elif type == 'critical':
            logger.critical(msg)

        print(f"[{type}] : {msg}")

        return True

    except Exception as e:
        print(f"Error in logging.py logging_msg(): {e}")
        return False