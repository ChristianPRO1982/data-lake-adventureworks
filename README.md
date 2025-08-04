# data-lake-adventureworks
Projet d'école : Extraction de données multi-sources pour alimenter un datalake
* table d'une BDD SQL-server
* Fichiers CSV compressés sur un data lake [Fichier de données]
* Autres Fichiers [Fichier de données]
* Fichiers Apache Parquet sur un data lake [Système big data]

## installation
à faire avant le *pip install -r requirements.txt*

Pour installer les dépendances nécessaires, exécutez la commande suivante dans bash et non dans zsh :

```bash
sudo apt-get update
sudo apt-get install libpq-dev python3-dev
sudo apt-get install unixodbc unixodbc-dev
sudo ACCEPT_EULA=Y apt install msodbcsql18
```

Faire une installation manuelle de unixodbc si besoin
```bash
tar -xzf unixODBC-2.3.12.tar.gz
cd unixODBC-2.3.12
./configure
make
sudo make install
```

si besoin, mettre à jour les fichiers */etc/odbcinst.ini* et */etc/odbc.ini*
```bash
ls /etc/odbcinst.ini /etc/odbc.ini
```
créer les fichiers manquants

MAJ de */etc/odbcinst.ini*
```bash
sudo nano /etc/odbcinst.ini
```
```ini
[ODBC Driver 18 for SQL Server]
Description=Microsoft ODBC Driver 18 for SQL Server
Driver=/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.0.so.1.1
UsageCount=1
```

MAJ de */etc/odbc.ini*
```bash
sudo nano /etc/odbc.ini
```
```ini
[MyDSN]
Description=My SQL Server Data Source
Driver=ODBC Driver 18 for SQL Server
Server=your_server_address
Database=your_database_name
```

pour tester
```bash
which odbcinst
odbcinst -q -d
```
*odbcinst -q -d* doit retourner le nom du driver utilisé

## organisation
ajout du CI/CD

mise en place de logs

ajout de la crontab à 2H00 du matin

```mermaid
flowchart LR
    crontab((crontab : ⏰2AM))
    crontab --> scheduling.sh

    subgraph shell
        scheduling.sh
        scheduling.sh --> extract_SQLserver.sh
        scheduling.sh --> extract_all_files.sh
        scheduling.sh --> extract_apache_parquet.sh
        scheduling.sh --> extract_CSV_compressed.sh
        scheduling.sh --> extract_other_files.sh
        scheduling.sh --> clean_up.sh
        scheduling.sh --> email.sh
    end

    subgraph python
        extract_SQLserver.sh --> extract_SQLserver.py:::python
        extract_all_files.sh --> extract_all_files.py:::python
        extract_apache_parquet.sh --> extract_apache_parquet.py:::python
        extract_CSV_compressed.sh --> extract_CSV_compressed.py:::python
        extract_other_files.sh --> extract_other_files.py:::python
        clean_up.sh --> clean_up.py:::python
        email.sh --> email.py:::python
    end

    subgraph datalake["Azure Cloud datalake"]
        extract_SQLserver.py --> DB[(SQL Server)]:::mysql
        extract_all_files.py --> files@{ shape: docs, label: "files" }
        files:::tfile
        extract_apache_parquet.py --> parquets@{ shape: docs, label: "parket files" }
        parquets:::tfile
        extract_CSV_compressed.py --> csv@{ shape: docs, label: "csv compressed" }
        csv:::tfile
        extract_other_files.py --> otherfiles@{ shape: docs, label: "other files" }
        otherfiles:::tfile
    end

    subgraph output
        DB o--o csvDB@{ shape: docs, label: "csv files" }
        csvDB:::tfile
        files o--o filesOUT@{ shape: docs, label: "files" }
        filesOUT:::tfile
        parquets o--o parquetsOUT@{ shape: docs, label: "parket files" }
        parquetsOUT:::tfile
        csv o--o csvOUT@{ shape: docs, label: "csv compressed" }
        csvOUT:::tfile
        otherfiles o--o otherfilesOUT@{ shape: docs, label: "other files" }
        otherfilesOUT:::tfile
    end


    classDef python fill:#FFDC52, color:#000;
    classDef fastapi fill:#059286, color:#45D2C6
    classDef openai fill:#FFF, color:#000;
    classDef mysql fill:#00618B, color:#40A1CB
    classDef sqlite fill:#4FC0FC, color:#0F80CC
    classDef file fill:#BBB, color:#333
    classDef tfile fill:#888, color:#333
```