import pandas as pd
import dotenv
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, text
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from source.logs import init_log, logging_msg



####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    log_prefix = '[ext-SQLserver | init]'
    try:
        init_log()
        dotenv.load_dotenv('.env', override=True)

        logging_msg(f"{log_prefix} OK")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False


##################
### CONNECTION ###
##################
def connect()->create_engine:
    log_prefix = '[ext-SQLserver | connect]'
    try:
        logging_msg(f"{log_prefix} init env variables", 'DEBUG')

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

        if not all([DRIVER, SERVER, DATABASE, UID, PWD]):
            raise ValueError("Missing required environment variables")
        
        logging_msg(f"{log_prefix} create connection string", 'DEBUG')
        connection_string = (
            f"mssql+pyodbc://{quote_plus(UID)}:{quote_plus(PWD)}@{SERVER},{1433}/{DATABASE}"
            f"?driver={quote_plus(DRIVER)}&encrypt={ENCRYPT}&TrustServerCertificate={TRUSTSERVERCERTIFICATE}"
            f"&timeout={CONNECTION_TIMEOUT}"
        )

        logging_msg(f"{log_prefix} create engine")
        engine = create_engine(connection_string)
        return engine
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return None
    

##################
### DISCONNECT ###
##################
def disconnect(engine:create_engine)->None:
    log_prefix = '[ext-SQLserver | disconnect]'
    try:
        logging_msg(f"{log_prefix} close engine")
        engine.dispose()
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return None


####################################################################################################
####################################################################################################
####################################################################################################

#######################################
### FIND ALL TABLES IN THE DATABASE ###
#######################################
def get_table_columns(schema, table, engine)->pd.DataFrame:
    log_prefix = '[ext-SQLserver | get_table_columns]'
    try:
        request = """
SELECT COLUMN_NAME, DATA_TYPE
  FROM INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_SCHEMA = :schema
   AND TABLE_NAME = :table
"""
        logging_msg(f"{log_prefix} request for {schema}.{table} OK", 'DEBUG')
        return pd.read_sql_query(text(request), engine, params={"schema": schema, "table": table})
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return None


######################################
### EXTRACT TABLES FROM SQL SERVER ###
######################################
def extract_tables(engine:create_engine)->bool:
    log_prefix = '[ext-SQLserver | extract_table]'
    try:
        logging_msg(f"{log_prefix} Find all tables in the database", 'DEBUG')
        
        SCHEMAS = os.getenv("SCHEMAS")
        DEBUG = os.getenv("DEBUG")

        request = f"""
SELECT *
  FROM INFORMATION_SCHEMA.TABLES
 WHERE table_schema IN ({SCHEMAS})
        """

        df_tables = pd.read_sql_query(text(request), engine)
        
        output_dir = './output/SQL-server/'
        os.makedirs(output_dir, exist_ok=True)
        
        count = 0
        for index, row in df_tables.iterrows():
            table_schema = row['TABLE_SCHEMA']
            table_name = row['TABLE_NAME']
            
            logging_msg(f"{log_prefix} Extracting table {table_schema}.{table_name}", 'DEBUG')
            
            df_columns = get_table_columns(table_schema, table_name, engine)
            if df_columns is None:
                logging_msg(f"{log_prefix} Error: get_table_columns({table_schema}, {table_name}, engine)", 'WARNING')

            else:
                select_columns = []
                for _, col in df_columns.iterrows():
                    column_name = col['COLUMN_NAME']
                    data_type = col['DATA_TYPE']
                    if data_type in ('geometry', 'geography'):
                        # Convert space columns to WKT
                        select_columns.append(f"{column_name}.STAsText() AS {column_name}_WKT")
                    else:
                        select_columns.append(column_name)
                
                select_clause = ", ".join(select_columns)
                table_query = f"SELECT {select_clause} FROM {table_schema}.{table_name}"
                
                try:
                    # extract and save the table on csv file
                    table_df = pd.read_sql_query(table_query, engine)
                    output_file = os.path.join(output_dir, f"{table_schema}.{table_name}.csv")
                    table_df.to_csv(output_file, index=False)
                    count += 1
                    logging_msg(f"{log_prefix} Table {table_schema}.{table_name} saved in {output_file}", 'DEBUG')

                except Exception as e:
                    logging_msg(f"{log_prefix} Error: {e}", 'WARNING')
                    continue
            
            if DEBUG == '1' and index >= 1:
                break
        
        logging_msg(f"{log_prefix} {count} tables saved of {len(df_tables)} tables")

    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False


############
### MAIN ###
############
def main()->bool:
    log_prefix = '[ext-SQLserver | main]'
    try:
        if init():
            engine = connect()
            if engine:
                extract_tables(engine)
            disconnect(engine)
            logging_msg(f"{log_prefix} ALL OK")
        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False