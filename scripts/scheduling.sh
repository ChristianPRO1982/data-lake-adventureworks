#!/bin/bash

# Navigate to the directory containing the Python script
cd /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks

# Activate the virtual environment
source /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks/venv/bin/activate

# Run the Python script (connection, extraction, diconnection)
python3 -c "from source.extract_SQLserver import main; main()"
