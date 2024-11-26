#!/bin/bash

# Navigate to the directory containing the Python script
cd /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks/source

# Activate the virtual environment
source /home/utilisateur/Documents/projects/DEV_IA/data-lake-adventureworks/venv/bin/activate

# Execute the Python script with the functions init() and connect()
python3 -c "from extract_SQLserver import init, connect; init(); connect()"