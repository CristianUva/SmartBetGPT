import sys
import os
import logging
import mysql.connector
from contextlib import contextmanager

# Configurazione logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# IMPORTANTE: Cambia questo percorso con il tuo username di PythonAnywhere
username = 'SmartBetGPT'  # Modifica con il tuo username effettivo
path = f'/home/{username}/mysite/SmartBetGPT'

logger.info(f"Impostazione percorso app: {path}")

if path not in sys.path:
    sys.path.append(path)

# Rileva se siamo su PythonAnywhere
is_pythonanywhere = 'PYTHONANYWHERE_SITE' in os.environ
os.environ['PYTHONANYWHERE_SITE'] = 'true'  # Imposta la variabile d'ambiente
os.environ['USE_MYSQL'] = 'true'  # Usa MySQL su PythonAnywhere

# Configurazione condizionale del database
if is_pythonanywhere:
    # Configurazione per PythonAnywhere
    db_config = {
        'user': 'SmartBetGPT',
        'password': 'Angelogalanti69',  
        'host': 'SmartBetGPT.mysql.pythonanywhere-services.com',
        'database': 'SmartBetGPT$database', 
        'raise_on_warnings': True
    }
    logger.info(f"Usando configurazione database per PythonAnywhere: {db_config['host']} - {db_config['database']}")
else:
    # Configurazione per ambiente locale
    db_config = {
        'user': 'root',
        'password': 'x',
        'host': 'localhost',
        'database': 'database',
        'raise_on_warnings': True
    }
    logger.info("Usando configurazione database per ambiente locale")

def get_db_connection():
    """Crea una connessione al database MySQL."""
    try:
        logger.info(f"Tentativo di connessione al database: {db_config['host']} - {db_config['database']}")
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        logger.error(f"Errore di connessione al database: {err}")
        raise

@contextmanager
def db_cursor(dictionary=True):
    """
    Context manager per gestire connessioni al database in modo sicuro.
    Garantisce la chiusura della connessione anche in caso di eccezioni.

    Args:
        dictionary (bool): Se True, restituisce i risultati come dizionari
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=dictionary)
        yield cursor, conn
        conn.commit()
    except Exception as e:
        logger.error(f"Errore nell'operazione sul database: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# PARTE CRUCIALE: Importa e crea l'applicazione Flask
try:
    logger.info("Importazione dell'applicazione Flask...")
    
    # Importa e crea l'applicazione Flask
    from app import create_app
    application = create_app()
    
    logger.info("Applicazione Flask creata con successo!")
except Exception as e:
    logger.error(f"Errore durante l'inizializzazione dell'applicazione: {e}")
    import traceback
    traceback.print_exc()
    raise e