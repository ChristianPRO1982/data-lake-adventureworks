#!/bin/bash

# Navigate to the directory containing the Python script
cd /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks

# Activate the virtual environment
source /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks/venv/bin/activate

# Run the Python script for extraxt SQLserver (connection, extraction, diconnection)
./scripts/extract_SQLserver.sh

# Run the Python script for extract files from Azure datalake (connection, extraction, diconnection)
./scripts/extract_all_files.sh

# Run extract png from parket files
./scripts/extract_apache_parquet.sh

# Run the Python script for csv files from the compressed file
./scripts/extract_CSV_compressed.sh

# Run the Python script for other files
./scripts/extract_other_files.sh

# clean the downloaded files and replace files in ML folder
./scripts/clean_up.sh
