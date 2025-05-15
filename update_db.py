# Script to update database structure and perform migrations
import os
import sys
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app, db
from models.user import User
from flask_migrate import Migrate, upgrade, init, migrate, stamp

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create app instance
app = create_app()

# Create migration instance
migrate_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
migrate = Migrate(app, db, directory=migrate_dir)

def init_migrations():
    """Initialize the migration repository if it doesn't exist."""
    if not os.path.exists(migrate_dir):
        logger.info("Inizializzazione repository migrazioni...")
        with app.app_context():
            init(directory=migrate_dir)
            stamp(directory=migrate_dir)
        logger.info("Repository migrazioni inizializzato.")

def create_migration():
    """Create a new migration based on model changes."""
    logger.info("Creazione di una nuova migrazione...")
    with app.app_context():
        migrate(directory=migrate_dir, message="Auto-generated migration")
    logger.info("Migrazione creata.")

def apply_migrations():
    """Apply all pending migrations."""
    logger.info("Applicazione migrazioni in corso...")
    with app.app_context():
        upgrade(directory=migrate_dir)
    logger.info("Migrazioni applicate con successo.")

def update_db():
    """Update the database structure using migrations."""
    try:
        # Detect DB type
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_type = 'MySQL' if 'mysql' in db_uri else 'SQLite'
        logger.info(f"Aggiornamento database {db_type}...")
        
        # Initialize migrations repository if needed
        init_migrations()
        
        # Try to update with create_all first (works for new databases)
        with app.app_context():
            db.create_all()
            
        # Create and apply migrations for schema changes
        create_migration()
        apply_migrations()
        
        logger.info("Database aggiornato con successo.")
    except Exception as e:
        logger.error(f"Errore durante l'aggiornamento del database: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    update_db()
