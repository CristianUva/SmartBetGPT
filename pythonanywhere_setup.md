# Guida alla configurazione su PythonAnywhere

Questa guida ti aiuterà a configurare SmartBetGPT su PythonAnywhere.

## 1. Crea un account PythonAnywhere

Se non hai ancora un account, registrati su [PythonAnywhere](https://www.pythonanywhere.com/).

## 2. Crea una web app

1. Vai alla dashboard di PythonAnywhere
2. Clicca sulla scheda "Web"
3. Clicca sul pulsante "Add a new web app"
4. Scegli il dominio (es. `tuousername.pythonanywhere.com`)
5. Seleziona "Manual configuration"
6. Seleziona Python 3.9 o 3.10

## 3. Carica il progetto

### Opzione 1: Usando Git

```bash
# Nella console di PythonAnywhere
git clone https://github.com/tuorepository/SmartBetGPT.git
```

### Opzione 2: Caricamento manuale

Carica i file tramite l'interfaccia di PythonAnywhere nella scheda "Files".

## 4. Configura le variabili d'ambiente

1. Vai alla scheda "Web"
2. Scorri verso il basso fino alla sezione "Environment variables"
3. Aggiungi le seguenti variabili:

```
PYTHONANYWHERE_SITE=true
SECRET_KEY=una_chiave_segreta_molto_complessa
EMAIL_USER=tuo_indirizzo_email@gmail.com
EMAIL_PASS=la_tua_password_applicazione
FOOTBALL_API_KEY=il_tuo_api_key_football_data

# Per MySQL (se necessario)
MYSQL_USER=SmartBetGPT
MYSQL_PASSWORD=LaTuaPassword
MYSQL_HOST=SmartBetGPT.mysql.pythonanywhere-services.com
MYSQL_DATABASE=SmartBetGPT$default
```

## 5. Configura il file WSGI

1. Vai alla scheda "Web"
2. Clicca sul link "WSGI configuration file" (es. `/var/www/tuousername_pythonanywhere_com_wsgi.py`)
3. Sostituisci il contenuto con:

```python
import sys
import os
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# IMPORTANTE: Cambia questo percorso con il tuo username di PythonAnywhere
username = 'tuousername'  # CAMBIA QUESTO con il tuo username di PythonAnywhere
path = f'/home/{username}/SmartBetGPT/SmartBetGPT'

logger.info(f"Impostazione percorso app: {path}")

if path not in sys.path:
    sys.path.append(path)

# Imposta la variabile d'ambiente per PythonAnywhere
os.environ['PYTHONANYWHERE_SITE'] = 'true'

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
```

## 6. Installa le dipendenze

Nella console di PythonAnywhere:

```bash
cd SmartBetGPT/SmartBetGPT
pip install -r requirements.txt
```

## 7. Crea il database

1. Nella console di PythonAnywhere:

```bash
cd SmartBetGPT/SmartBetGPT
python create_db.py
```

## 8. Configura il database MySQL (obbligatorio)

1. Vai alla scheda "Databases" nel pannello di controllo PythonAnywhere
2. Inizializza un nuovo database MySQL
   - Inserisci una password sicura quando richiesto
   - Il database verrà creato nel formato `tuousername$default` automaticamente

3. Configura le variabili d'ambiente per MySQL in "Web" → "Environment variables":
   ```
   MYSQL_USER=tuousername
   MYSQL_PASSWORD=la_password_che_hai_scelto
   MYSQL_HOST=tuousername.mysql.pythonanywhere-services.com
   MYSQL_DATABASE=tuousername$default
   ```

4. Installa le dipendenze necessarie:
   ```bash
   cd SmartBetGPT/SmartBetGPT
   pip install -r requirements.txt
   ```

5. Verifica la connessione al database:
   ```bash
   cd SmartBetGPT/SmartBetGPT
   python test_mysql_connection.py
   ```

6. Se il test ha avuto successo, crea la struttura del database:
   ```bash
   cd SmartBetGPT/SmartBetGPT
   python create_db.py
   ```

7. Se stai migrando da un database SQLite esistente, esegui lo script di migrazione:
   ```bash
   cd SmartBetGPT/SmartBetGPT
   python migrate_to_mysql.py
   ```
   
8. In caso di aggiornamenti futuri alla struttura del database, usa lo script di aggiornamento:
   ```bash
   cd SmartBetGPT/SmartBetGPT
   python update_db.py
   ```

## 9. Riavvia l'applicazione

1. Vai alla scheda "Web"
2. Clicca sul pulsante "Reload"

## 10. Verifica che tutto funzioni

Visita il tuo sito web all'indirizzo `https://tuousername.pythonanywhere.com` per verificare che tutto funzioni correttamente.

## Risoluzione dei problemi

### Log dell'applicazione

In caso di errori, controlla i log dell'applicazione nella scheda "Web" cliccando sui link "Error log" e "Server log".

### Permessi dei file

Assicurati che la directory del database abbia i permessi di scrittura:

```bash
chmod -R 755 /home/tuousername/SmartBetGPT/SmartBetGPT
```

### Problemi di connessione al database

Se riscontri problemi di connessione al database MySQL, verifica che le credenziali siano corrette nelle variabili d'ambiente.
