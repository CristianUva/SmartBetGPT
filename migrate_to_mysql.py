# migrate_to_mysql.py - Script per migrare i dati da SQLite a MySQL
import os
import sys
import sqlite3
import pymysql
import logging
from dotenv import load_dotenv

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carica variabili d'ambiente
load_dotenv()

def connect_to_sqlite(db_path):
    """Connessione al database SQLite"""
    try:
        logger.info(f"Connessione al database SQLite: {db_path}")
        return sqlite3.connect(db_path)
    except Exception as e:
        logger.error(f"Errore nella connessione al database SQLite: {e}")
        sys.exit(1)

def connect_to_mysql():
    """Connessione al database MySQL"""
    try:
        # Rileva se siamo su PythonAnywhere
        is_pythonanywhere = 'PYTHONANYWHERE_SITE' in os.environ
        
        if is_pythonanywhere:
            # Configurazione per PythonAnywhere
            mysql_config = {
                'user': os.environ.get('MYSQL_USER', 'SmartBetGPT'),
                'password': os.environ.get('MYSQL_PASSWORD', 'Angelogalanti69'),
                'host': os.environ.get('MYSQL_HOST', 'SmartBetGPT.mysql.pythonanywhere-services.com'),
                'database': os.environ.get('MYSQL_DATABASE', 'SmartBetGPT$database'),
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
            logger.info(f"Connessione a MySQL su PythonAnywhere: {mysql_config['host']}")
        else:
            # Configurazione per ambiente locale
            mysql_config = {
                'user': os.environ.get('MYSQL_USER_LOCAL', 'root'),
                'password': os.environ.get('MYSQL_PASSWORD_LOCAL', 'x'),
                'host': os.environ.get('MYSQL_HOST_LOCAL', 'localhost'),
                'database': os.environ.get('MYSQL_DATABASE_LOCAL', 'smartbetgpt'),
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
            logger.info(f"Connessione a MySQL locale: {mysql_config['host']}")

        return pymysql.connect(**mysql_config)
    except Exception as e:
        logger.error(f"Errore nella connessione al database MySQL: {e}")
        sys.exit(1)

def get_table_structure(sqlite_conn, table_name):
    """Ottiene la struttura di una tabella SQLite"""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return columns

def get_table_data(sqlite_conn, table_name):
    """Ottiene i dati di una tabella SQLite"""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows

def migrate_table(sqlite_conn, mysql_conn, table_name):
    """Migra una tabella da SQLite a MySQL"""
    logger.info(f"Migrazione tabella: {table_name}")
    
    try:
        # Ottieni struttura della tabella
        columns = get_table_structure(sqlite_conn, table_name)
        column_names = [col[1] for col in columns]
        
        # Ottieni dati della tabella
        rows = get_table_data(sqlite_conn, table_name)
        
        if not rows:
            logger.info(f"Nessun dato da migrare per la tabella {table_name}")
            return
        
        # Prepara query di inserimento
        placeholders = ", ".join(["%s"] * len(column_names))
        columns_str = ", ".join([f"`{col}`" for col in column_names])
        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # Inserisci i dati in MySQL
        cursor = mysql_conn.cursor()
        cursor.executemany(insert_query, rows)
        mysql_conn.commit()
        
        logger.info(f"Migrati {len(rows)} record nella tabella {table_name}")
    except Exception as e:
        logger.error(f"Errore durante la migrazione della tabella {table_name}: {e}")
        raise

def get_sqlite_tables(sqlite_conn):
    """Ottieni lista delle tabelle in SQLite"""
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

def migrate_database():
    """Migra l'intero database da SQLite a MySQL"""
    # Percorso al database SQLite - modifica se necessario
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'database.db')
    
    logger.info("Inizio migrazione da SQLite a MySQL")
    
    # Connessione ai database
    sqlite_conn = connect_to_sqlite(db_path)
    mysql_conn = connect_to_mysql()
    
    try:
        # Ottieni lista delle tabelle
        tables = get_sqlite_tables(sqlite_conn)
        logger.info(f"Tabelle trovate: {', '.join(tables)}")
        
        # Migra ogni tabella
        for table in tables:
            migrate_table(sqlite_conn, mysql_conn, table)
        
        logger.info("Migrazione completata con successo")
    except Exception as e:
        logger.error(f"Errore durante la migrazione: {e}")
    finally:
        sqlite_conn.close()
        mysql_conn.close()

if __name__ == "__main__":
    migrate_database()
