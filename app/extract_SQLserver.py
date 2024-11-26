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



############
### INIT ###
############
dotenv.load_dotenv('./.env', override=True)

DRIVER = os.getenv("DRIVER")
SERVER = os.getenv("SERVER")
if SERVER.startswith("tcp:"):
    SERVER = SERVER.replace("tcp:", "") # Alchemy doesn't like the tcp: prefix
DATABASE = os.getenv("DATABASE")
UID = os.getenv("UID")
PWD = os.getenv("PWD")
ENCRYPT = os.getenv("ENCRYPT")
TRUSTSERVERCERTIFICATE = os.getenv("TRUSTSERVERCERTIFICATE")
CONNECTION_TIMEOUT = os.getenv("CONNECTION_TIMEOUT")