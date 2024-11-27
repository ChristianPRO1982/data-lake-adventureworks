from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions, BlobClient, ContainerClient
from datetime import datetime, timedelta
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
    log_prefix = '[ext-all_files | init]'
    try:
        init_log()
        dotenv.load_dotenv('.env', override=True)

        logging_msg(f"{log_prefix} OK")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_sas_token()->bool:
    log_prefix = '[ext-all_files | init]'
    try:
        logging_msg(f"{log_prefix} START")

        account_name = os.getenv("DATALAKENAME")
        account_key = os.getenv("DATALAKEKEY")
        container_name = os.getenv("BLOBCONTAINER")

        sas_token = generate_container_sas(
            account_name=account_name,
            container_name=container_name,
            account_key=account_key,
            permission=ContainerSasPermissions(read=True, list=True),
            expiry=datetime.utcnow() + timedelta(hours=1)  # Expiration dans 1 heure
        )

        secrets_dir = os.path.join(os.path.dirname(__file__), '../secrets')
        os.makedirs(secrets_dir, exist_ok=True)
        with open(os.path.join(secrets_dir, 'token.txt'), 'w') as token_file:
            token_file.write(f"https://{account_name}.blob.core.windows.net/{container_name}?{sas_token}")

        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False


def get_sas_token_from_file()->str:
    log_prefix = '[ext-all_files | get_sas_token_from_file]'
    try:
        logging_msg(f"{log_prefix} START")

        secrets_dir = os.path.join(os.path.dirname(__file__), '../secrets')
        token_file_path = os.path.join(secrets_dir, 'token.txt')
        
        if not os.path.exists(token_file_path):
            raise FileNotFoundError("Token file not found")

        with open(token_file_path, 'r') as token_file:
            sas_token = token_file.read().strip()

        return sas_token
    
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'INFO')
        return ""


####################################################################################################
####################################################################################################
####################################################################################################

def extract_all_files(sas_url: str, folfer: str, target_folder: str)->bool:
    log_prefix = '[ext-all_files | extract_all_files]'
    try:
        logging_msg(f"{log_prefix} START")

        os.makedirs(target_folder, exist_ok=True)

        container_client = ContainerClient.from_container_url(sas_url)

        blobs = container_client.list_blobs(name_starts_with=folfer)
        # Télécharger les blobs
        for blob in blobs:
            blob_name = blob.name
            print('>>>', blob_name)
            # local_file_path = os.path.join(target_folder, os.path.basename(blob_name))
            # print(f"Téléchargement de {blob_name} vers {local_file_path}...")
            
            # # Télécharger le fichier
            # blob_client = container_client.get_blob_client(blob_name)
            # with open(local_file_path, "wb") as file:
            #     file.write(blob_client.download_blob().readall())

        # print("Téléchargement terminé.")

        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} {e}", 'CRITICAL')
        return False


####################################################################################################
####################################################################################################
####################################################################################################

############
### MAIN ###
############
def main()->bool:
    log_prefix = '[ext-all_files | main]'
    try:
        if init():
            sas_url = get_sas_token_from_file()
            if not sas_url:
                if generate_sas_token():
                    sas_url = get_sas_token_from_file()
                    if not sas_url:
                        raise Exception("Failed to get SAS token from file")
                else:
                    raise Exception("Failed to generate SAS token")

            folders = os.getenv("FOLDERS")
            folder_pairs = folders.split(',')
            for pair in folder_pairs:
                azure_folder, target_folder = pair.split(':')
                extract_all_files(sas_url, azure_folder, target_folder)

        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False