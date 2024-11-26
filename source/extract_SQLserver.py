import pyarrow as pa
import pandas as pd
import numpy as np
import dotenv
import pyodbc
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from .logging import init_log, logging_msg



############
### INIT ###
############
def init()->bool:
    log_prefix = '[ext-SQLserver | init]'
    try:
        init_log()
        dotenv.load_dotenv('../.env', override=True)

        logging_msg(f"{log_prefix} init() OK")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        logging_msg(f"{log_prefix} init() Error: {e}")
        return False


##################
### CONNECTION ###
##################
def connect()->create_engine:
    log_prefix = '[ext-SQLserver | connect]'
    try:
        logging_msg(f"{log_prefix} connect() : init env variables", 'DEBUG')

        DRIVER = os.getenv("DRIVER")
        SERVER = os.getenv("SERVER")
        if SERVER.startswith("tcp:"):  # Nettoyage de l'adresse serveur
            SERVER = SERVER.replace("tcp:", "")
        print(SERVER)
        DATABASE = os.getenv("DATABASE")
        UID = os.getenv("UID")
        PWD = os.getenv("PWD")
        ENCRYPT = os.getenv("ENCRYPT")
        TRUSTSERVERCERTIFICATE = os.getenv("TRUSTSERVERCERTIFICATE")
        CONNECTION_TIMEOUT = os.getenv("CONNECTION_TIMEOUT")

        
        logging_msg(f"{log_prefix} connect() : create connection string", 'DEBUG')
        connection_string = (
            f"mssql+pyodbc://{quote_plus(UID)}:{quote_plus(PWD)}@{SERVER},{1433}/{DATABASE}"
            f"?driver={quote_plus(DRIVER)}&encrypt={ENCRYPT}&TrustServerCertificate={TRUSTSERVERCERTIFICATE}"
            f"&timeout={CONNECTION_TIMEOUT}"
        )

        logging_msg(f"{log_prefix} connect() : create engine")
        engine = create_engine(connection_string)
        return engine
    
    except Exception as e:
        print(f"Error: {e}")
        return None