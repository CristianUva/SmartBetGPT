#!/bin/bash
# SmartBetGPT - Script di deployment per PythonAnywhere
# Uso: bash deploy_pythonanywhere.sh

echo "======================================================================"
echo "          Script di Deployment SmartBetGPT per PythonAnywhere         "
echo "======================================================================"
echo ""

# Imposta le variabili di configurazione
USERNAME="cristianuva"
PASSWORD="Angelogalanti69"
DATABASE_NAME="smartbetgpt"
APP_NAME="SmartBetGPT"
GIT_REPO="$HOME/$APP_NAME" # Percorso locale del repository

echo "Configurazione per l'utente: $USERNAME"
echo "Database: $DATABASE_NAME"
echo ""

# 1. Aggiorna il repository Git se già clonato, altrimenti lo clona
echo "[1/7] Preparazione del repository del progetto..."
if [ -d "$GIT_REPO" ]; then
    echo "Repository già esistente, aggiornamento in corso..."
    cd "$GIT_REPO"
    git pull
else
    echo "Clonazione del repository in corso..."
    git clone https://github.com/tuousername/SmartBetGPT.git "$GIT_REPO"
    cd "$GIT_REPO"
fi
echo "Repository pronto."
echo ""

# 2. Configura l'ambiente virtuale Python
echo "[2/7] Configurazione dell'ambiente Python..."
mkvirtualenv --python=python3.10 smartbetgpt-env
workon smartbetgpt-env

# 3. Installazione delle dipendenze
echo "[3/7] Installazione delle dipendenze..."
pip install --upgrade pip
pip install -r requirements.txt
pip install mysqlclient  # Assicuriamo che mysqlclient sia installato per PythonAnywhere
echo "Dipendenze installate con successo."
echo ""

# 4. Configurazione del file WSGI
echo "[4/7] Configurazione del file WSGI..."
WSGI_PATH="/var/www/${USERNAME}_pythonanywhere_com_wsgi.py"
echo "Creazione del file WSGI in: $WSGI_PATH"

# Creazione del contenuto del file WSGI corretto
cat > "$HOME/wsgi_file.py" << EOF
import sys
import os
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurazione percorso dell'applicazione
username = "$USERNAME"
path = f'/home/{username}/$APP_NAME'

logger.info(f"Impostazione percorso app: {path}")

if path not in sys.path:
    sys.path.append(path)

# Imposta le variabili d'ambiente per PythonAnywhere
os.environ['PYTHONANYWHERE_SITE'] = 'true'
os.environ['USE_MYSQL'] = 'true'

# Configurazione del database
os.environ['MYSQL_USER'] = '$USERNAME'
os.environ['MYSQL_PASSWORD'] = '$PASSWORD'
os.environ['MYSQL_HOST'] = '$USERNAME.mysql.pythonanywhere-services.com'
os.environ['MYSQL_DATABASE'] = '$USERNAME\$$DATABASE_NAME'

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

echo "File WSGI creato con successo."
echo ""

# 5. Configura il database MySQL
echo "[5/7] Configurazione del database MySQL..."
echo "NOTA: È necessario creare manualmente il database dal pannello di controllo di PythonAnywhere"
echo "Vai alla scheda 'Databases', crea un nuovo database MySQL e annota le credenziali"
echo ""

# 6. Verifica connessione database e inizializza
echo "[6/7] Verifica della connessione al database e inizializzazione..."
echo "python -c \"import os; os.environ['PYTHONANYWHERE_SITE'] = 'true'; os.environ['MYSQL_USER'] = '$USERNAME'; os.environ['MYSQL_PASSWORD'] = '$PASSWORD'; os.environ['MYSQL_HOST'] = '$USERNAME.mysql.pythonanywhere-services.com'; os.environ['MYSQL_DATABASE'] = '$USERNAME\$$DATABASE_NAME'; from test_mysql_connection import test_connection; test_connection()\""
echo ""

# 7. Istruzioni per completare la configurazione
echo "[7/7] Istruzioni finali per completare la configurazione..."
echo ""
echo "===================================================================================="
echo "  CONFIGURAZIONE MANUALE RICHIESTA"
echo "===================================================================================="
echo ""
echo "1. Copia il file WSGI generato:"
echo "   - Vai alla scheda 'Web' su PythonAnywhere"
echo "   - Fai clic su 'WSGI configuration file' (es. /var/www/${USERNAME}_pythonanywhere_com_wsgi.py)"
echo "   - Sostituisci il contenuto con il file wsgi_file.py creato in $HOME/wsgi_file.py"
echo ""
echo "2. Imposta il percorso dell'app web:"
echo "   - Nella scheda 'Web', imposta 'Source code' su: $HOME/$APP_NAME"
echo "   - Imposta 'Working directory' su: $HOME/$APP_NAME"
echo ""
echo "3. Imposta le variabili d'ambiente:"
echo "   - Nella scheda 'Web', scorri fino a 'Environment variables'"
echo "   - Aggiungi almeno queste variabili:"
echo "     PYTHONANYWHERE_SITE=true"
echo "     SECRET_KEY=una_chiave_complessa_e_sicura"
echo "     MYSQL_USER=$USERNAME"
echo "     MYSQL_PASSWORD=$PASSWORD"
echo "     MYSQL_HOST=$USERNAME.mysql.pythonanywhere-services.com"
echo "     MYSQL_DATABASE=$USERNAME\$$DATABASE_NAME"
echo ""
echo "4. Inizializza il database:"
echo "   - Esegui questi comandi nella console PythonAnywhere:"
echo "     cd $HOME/$APP_NAME"
echo "     python create_db.py"
echo ""
echo "5. Riavvia l'applicazione web:"
echo "   - Fai clic sul pulsante 'Reload' nella scheda 'Web'"
echo ""
echo "6. Verifica che tutto funzioni correttamente:"
echo "   - Visita il tuo sito all'indirizzo: https://$USERNAME.pythonanywhere.com"
echo ""
echo "===================================================================================="
echo ""
echo "Completato!"
