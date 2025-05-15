"""
Configurazione WSGI per PythonAnywhere
Questo file viene utilizzato da PythonAnywhere per avviare l'applicazione.
"""
import sys
import os
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# IMPORTANTE: Cambia questo percorso con il tuo username di PythonAnywhere
username = 'cristianuva'  # Cambia con il tuo username di PythonAnywhere
path = f'/home/cristianuva/SmartBetGPT/SmartBetGPT'

logger.info(f"Impostazione percorso app: {path}")

if path not in sys.path:
    sys.path.append(path)

# Imposta la variabile d'ambiente per PythonAnywhere
os.environ['PYTHONANYWHERE_SITE'] = 'true'

# Imposta la variabile per specificare di usare MySQL
os.environ['USE_MYSQL'] = 'true'

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

if __name__ == '__main__':
    application.run()
