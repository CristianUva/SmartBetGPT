# create_db.py - Database initialization script
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app, db
from models.user import User
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Inizializzazione database...")

# Rileva se siamo su PythonAnywhere
is_pythonanywhere = 'PYTHONANYWHERE_SITE' in os.environ

# Crea l'applicazione Flask
app = create_app()

with app.app_context():
    try:
        # Check if we're using SQLite or MySQL
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_type = 'MySQL' if 'mysql' in db_uri else 'SQLite'
        
        logger.info(f"Configurazione database: {db_type}")
        
        # Se è SQLite, assicurati che il file esista
        if db_type == 'SQLite':
            import sqlite3
            # Extracting SQLite file path from URI
            db_path = db_uri.replace('sqlite:///', '')
            
            # Create directory if not exists
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                
            if not os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                logger.info(f"Database SQLite creato: {db_path}")
                conn.close()
        
        # Create all tables defined in models
        db.create_all()
        logger.info("Tabelle create con successo nel database")
        
        # You can add initial data here if needed
        
    except Exception as e:
        logger.error(f"Errore durante l'inizializzazione del database: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("Processo di inizializzazione database completato con successo.")
