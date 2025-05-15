# test_mysql_connection.py - Script per testare la connessione a MySQL
import os
import sys
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carica variabili d'ambiente
load_dotenv()

def test_mysql_connection():
    """Testa la connessione a MySQL"""
    try:
        # Rileva se siamo su PythonAnywhere
        is_pythonanywhere = 'PYTHONANYWHERE_SITE' in os.environ
        
        if is_pythonanywhere:
            # Configurazione per PythonAnywhere
            mysql_user = os.environ.get('MYSQL_USER', 'cristianuva')
            mysql_password = os.environ.get('MYSQL_PASSWORD', 'Angelogalanti69')
            mysql_host = os.environ.get('MYSQL_HOST', 'cristianuva.mysql.pythonanywhere-services.com')
            mysql_db = os.environ.get('MYSQL_DATABASE', 'cristianuva$default')
        else:
            # Configurazione per ambiente locale
            mysql_user = os.environ.get('MYSQL_USER_LOCAL', 'root')
            mysql_password = os.environ.get('MYSQL_PASSWORD_LOCAL', 'x')
            mysql_host = os.environ.get('MYSQL_HOST_LOCAL', 'localhost')
            mysql_db = os.environ.get('MYSQL_DATABASE_LOCAL', 'smartbetgpt')
        
        # Crea URL di connessione
        db_uri = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
        
        logger.info(f"Tentativo di connessione a MySQL: {mysql_host}/{mysql_db}")
        
        # Crea engine SQLAlchemy
        engine = create_engine(db_uri)
        
        # Testa la connessione
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            row = result.fetchone()
            if row[0] == 1:
                logger.info("Connessione a MySQL stabilita con successo!")
                
                # Visualizza le tabelle nel database
                result = connection.execute(text('SHOW TABLES'))
                tables = result.fetchall()
                if tables:
                    logger.info(f"Tabelle nel database: {', '.join([t[0] for t in tables])}")
                else:
                    logger.info("Nessuna tabella trovata nel database")
                    
                return True
    except Exception as e:
        logger.error(f"Errore durante la connessione a MySQL: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_mysql_connection():
        logger.info("Test di connessione MySQL completato con successo")
        sys.exit(0)
    else:
        logger.error("Test di connessione MySQL fallito")
        sys.exit(1)
