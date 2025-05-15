#!/bin/bash
# Script di deploy rapido per SmartBetGPT su PythonAnywhere
# Salva questo file come deploy_quick.sh e eseguilo sulla console PythonAnywhere

echo "======================================================="
echo "     DEPLOY RAPIDO SMARTBETGPT SU PYTHONANYWHERE       "
echo "======================================================="
echo ""

# Configurazione dell'utente - MODIFICARE CON I PROPRI DATI!
USERNAME="cristianuva"
PASSWORD="Angelogalanti69"
DATABASE="smartbetgpt"

echo "Username: $USERNAME"
echo "Database: $USERNAME\$$DATABASE"
echo ""

# Cartella di lavoro
cd ~

# Clona o aggiorna il repository
if [ -d "SmartBetGPT" ]; then
    echo "[1/7] Aggiornamento repository esistente..."
    cd SmartBetGPT
    git pull
else
    echo "[1/7] Clonazione repository..."
    # Sostituisci con il tuo URL Git se ne hai uno
    git clone https://github.com/tuousername/SmartBetGPT.git
    cd SmartBetGPT
fi

# Crea e attiva l'ambiente virtuale
echo "[2/7] Configurazione ambiente virtuale..."
if [ -d "$HOME/.virtualenvs/smartbetgpt-env" ]; then
    echo "Ambiente virtuale già esistente, attivazione..."
    source $HOME/.virtualenvs/smartbetgpt-env/bin/activate
else
    echo "Creazione nuovo ambiente virtuale..."
    mkvirtualenv --python=python3.10 smartbetgpt-env
    workon smartbetgpt-env
fi

# Installa dipendenze
echo "[3/7] Installazione dipendenze..."
pip install --upgrade pip
pip install -r requirements.txt
pip install mysqlclient

# Crea file WSGI corretto
echo "[4/7] Creazione file WSGI di configurazione..."
cat > cristianuva_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurazione percorso dell'applicazione
username = "cristianuva"
path = f'/home/{username}/SmartBetGPT'

logger.info(f"Impostazione percorso app: {path}")

if path not in sys.path:
    sys.path.append(path)

# Imposta le variabili d'ambiente per PythonAnywhere
os.environ['PYTHONANYWHERE_SITE'] = 'true'
os.environ['USE_MYSQL'] = 'true'

# Configurazione del database
os.environ['MYSQL_USER'] = 'cristianuva'
os.environ['MYSQL_PASSWORD'] = 'Angelogalanti69'
os.environ['MYSQL_HOST'] = 'cristianuva.mysql.pythonanywhere-services.com'
os.environ['MYSQL_DATABASE'] = 'cristianuva$smartbetgpt'

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
EOF

echo "File WSGI creato! Ora devi copiarlo manualmente in /var/www/${USERNAME}_pythonanywhere_com_wsgi.py"
echo ""

# Test della connessione al database
echo "[5/7] Test connessione al database..."
echo "Impostazione variabili d'ambiente per il test..."
export PYTHONANYWHERE_SITE=true
export MYSQL_USER=$USERNAME
export MYSQL_PASSWORD=$PASSWORD
export MYSQL_HOST=$USERNAME.mysql.pythonanywhere-services.com
export MYSQL_DATABASE=$USERNAME\$$DATABASE

echo "Tentativo di connessione al database..."
echo "NOTA: Questo comando potrebbe fallire se il database non è stato ancora creato."
python -c "
import os, sys, mysql.connector
try:
    conn = mysql.connector.connect(
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        host=os.environ.get('MYSQL_HOST'),
        database=os.environ.get('MYSQL_DATABASE')
    )
    print('Connessione al database riuscita!')
    conn.close()
except Exception as e:
    print(f'Errore di connessione: {e}')
    print('Verifica di aver creato il database dalla sezione Databases di PythonAnywhere')
    sys.exit(1)
"

# Inizializzazione del database
echo "[6/7] Inizializzazione del database..."
echo "python create_db.py"
echo "NOTA: Esegui questo comando manualmente dopo aver verificato la connessione al database"
echo ""

# Istruzioni finali
echo "[7/7] Istruzioni finali..."
echo ""
echo "============================================================="
echo "AZIONI MANUALI NECESSARIE PER COMPLETARE IL DEPLOY:"
echo "============================================================="
echo ""
echo "1. Vai alla sezione 'Web' di PythonAnywhere"
echo "2. Configura la tua Web App:"
echo "   - Source code: $HOME/SmartBetGPT"
echo "   - Working directory: $HOME/SmartBetGPT"
echo "   - Virtualenv: $HOME/.virtualenvs/smartbetgpt-env"
echo "3. Copia il contenuto di $HOME/SmartBetGPT/cristianuva_pythonanywhere_com_wsgi.py"
echo "   nel file WSGI di PythonAnywhere (/var/www/${USERNAME}_pythonanywhere_com_wsgi.py)"
echo "4. Imposta le variabili d'ambiente nella sezione 'Web':"
echo "   - PYTHONANYWHERE_SITE=true"
echo "   - SECRET_KEY=una_chiave_molto_sicura_e_complessa"
echo "   - MYSQL_USER=$USERNAME"
echo "   - MYSQL_PASSWORD=$PASSWORD"
echo "   - MYSQL_HOST=$USERNAME.mysql.pythonanywhere-services.com"
echo "   - MYSQL_DATABASE=$USERNAME\$$DATABASE"
echo "5. Crea un database MySQL nella sezione 'Databases' se non l'hai già fatto"
echo "6. Esegui 'python create_db.py' nella console di PythonAnywhere"
echo "7. Riavvia l'applicazione con il pulsante 'Reload' nella sezione 'Web'"
echo ""
echo "============================================================="
echo "Guida completa disponibile in: $HOME/SmartBetGPT/TUTORIAL_DEPLOY_PYTHONANYWHERE.md"
echo "============================================================="
