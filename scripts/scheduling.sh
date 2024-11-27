#!/bin/bash

# Navigate to the directory containing the Python script
cd /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks

# Activate the virtual environment
source /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks/venv/bin/activate

# Run the Python script for extraxt SQLserver (connection, extraction, diconnection)
# ./scripts/extract_SQLserver.sh

# Run the Python script for extract files from Azure datalake (connection, extraction, diconnection)
./scripts/extract_all_files.sh
