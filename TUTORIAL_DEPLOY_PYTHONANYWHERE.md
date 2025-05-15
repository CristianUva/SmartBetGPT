# GUIDA COMPLETA PER IL DEPLOY DI SMARTBETGPT SU PYTHONANYWHERE

Questa guida ti guiderà passo-passo attraverso il processo di deployment di SmartBetGPT su PythonAnywhere, con configurazioni specifiche per il tuo account.

## INFORMAZIONI ACCOUNT
- **Username PythonAnywhere**: cristianuva
- **Database**: smartbetgpt
- **Percorso App**: /home/cristianuva/SmartBetGPT

## PREREQUISITI
- Un account su PythonAnywhere (livello gratuito è sufficiente per cominciare)
- Il codice sorgente di SmartBetGPT (già nel tuo account GitHub o locale)

## PROCEDURA DI DEPLOY

### 1. ACCESSO E PREPARAZIONE

1. Accedi al tuo account PythonAnywhere su [pythonanywhere.com](https://www.pythonanywhere.com) usando:
   - Username: cristianuva
   - Password: Angelogalanti69

2. Una volta entrato, apri una nuova console Bash cliccando su "Consoles" > "New Console" > "Bash"

### 2. CLONA IL REPOSITORY

In alternativa, se il progetto è già sul tuo GitHub:

```bash
cd ~
git clone https://github.com/tuousername/SmartBetGPT.git
```

Se hai già i file localmente, puoi utilizzare l'upload nella sezione "Files" di PythonAnywhere.

### 3. CREA UN AMBIENTE VIRTUALE PYTHON

```bash
cd ~
mkvirtualenv --python=python3.10 smartbetgpt-env
workon smartbetgpt-env
```

### 4. INSTALLA LE DIPENDENZE

```bash
cd ~/SmartBetGPT
pip install --upgrade pip
pip install -r requirements.txt
pip install mysqlclient
```

### 5. CONFIGURA IL DATABASE MYSQL

1. Vai alla scheda "Databases" nel pannello di controllo
2. Nella sezione MySQL, crea un nuovo database:
   - Inserisci la password: Angelogalanti69
   - Clicca su "Initialize MySQL"
   - Crea un nuovo database: smartbetgpt

Il tuo database sarà disponibile come: `cristianuva$smartbetgpt`

### 6. CREA UNA WEB APP

1. Vai alla scheda "Web"
2. Clicca su "Add a new web app"
3. Scegli il dominio (cristianuva.pythonanywhere.com)
4. Seleziona "Manual configuration"
5. Scegli Python 3.10
6. Clicca su "Next"

### 7. CONFIGURA LA WEB APP

Nella pagina di configurazione della web app:

1. **Source code**: Imposta il percorso del codice sorgente:
   ```
   /home/cristianuva/SmartBetGPT
   ```

2. **Working directory**: Usa lo stesso percorso:
   ```
   /home/cristianuva/SmartBetGPT
   ```

3. **WSGI configuration file**:
   - Clicca sul link al file WSGI (es. `/var/www/cristianuva_pythonanywhere_com_wsgi.py`)
   - Sostituisci tutto il contenuto con:

```python
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
```

4. **Ambiente virtuale**: Nella sezione "Virtualenv", imposta il percorso:
   ```
   /home/cristianuva/.virtualenvs/smartbetgpt-env
   ```

5. **Variabili d'ambiente**: Nella sezione "Environment variables", aggiungi:
   
   ```
   PYTHONANYWHERE_SITE=true
   SECRET_KEY=una_chiave_molto_sicura_e_complessa
   MYSQL_USER=cristianuva
   MYSQL_PASSWORD=Angelogalanti69
   MYSQL_HOST=cristianuva.mysql.pythonanywhere-services.com
   MYSQL_DATABASE=cristianuva$smartbetgpt
   ```

   Se utilizzi servizi email, aggiungi anche:
   ```
   MAIL_USERNAME=tua_email@gmail.com
   MAIL_PASSWORD=la_tua_password_applicazione
   MAIL_DEFAULT_SENDER=tua_email@gmail.com
   ```

### 8. INIZIALIZZA IL DATABASE

Nel terminale Bash di PythonAnywhere:

```bash
cd ~/SmartBetGPT
workon smartbetgpt-env
python create_db.py
```

### 9. VERIFICA LA CONNESSIONE AL DATABASE

```bash
cd ~/SmartBetGPT
workon smartbetgpt-env
python test_mysql_connection.py
```

### 10. RIAVVIA L'APPLICAZIONE

Torna alla scheda "Web" e clicca sul pulsante "Reload"

### 11. VERIFICA IL DEPLOYMENT

Visita il tuo sito all'indirizzo:
```
https://cristianuva.pythonanywhere.com
```

## RISOLUZIONE DEI PROBLEMI

### Verifica i log degli errori

Nella scheda "Web", puoi verificare:
- Error log
- Server log
- Access log

### Problemi comuni e soluzioni

1. **Errori di importazione dei moduli**:
   - Assicurati che il percorso del progetto sia corretto nel file WSGI
   - Controlla che tutte le dipendenze siano installate

2. **Errori di database**:
   - Verifica le credenziali del database nelle variabili d'ambiente
   - Controlla che il database sia stato creato correttamente
   - Esegui nuovamente `python test_mysql_connection.py` per verificare la connessione

3. **Permessi dei file**:
   - Assicurati che tutti i file abbiano i permessi corretti:
   ```bash
   chmod -R 755 ~/SmartBetGPT
   ```

4. **Errori di avvio**:
   - Verifica i log dell'applicazione per identificare il problema
   - Prova a eseguire l'applicazione in modalità debug nella console

## AGGIORNAMENTI FUTURI

Per aggiornare l'applicazione in futuro:

1. Aggiorna il codice sorgente:
   ```bash
   cd ~/SmartBetGPT
   git pull
   ```

2. Installa eventuali nuove dipendenze:
   ```bash
   workon smartbetgpt-env
   pip install -r requirements.txt
   ```

3. Aggiorna il database (se necessario):
   ```bash
   python update_db.py
   ```

4. Riavvia l'applicazione dalla scheda "Web"

## NOTE IMPORTANTI

1. L'account gratuito di PythonAnywhere ha limitazioni di risorse e traffico
2. L'applicazione va in sospensione dopo un periodo di inattività, il primo caricamento potrebbe essere lento
3. Backup regolari del database sono consigliati

## UTILIZZO DELLO SCRIPT DI DEPLOY AUTOMATIZZATO

Per automatizzare parte del processo, abbiamo creato uno script di deploy:

```bash
cd ~/SmartBetGPT
chmod +x deploy_pythonanywhere.sh
./deploy_pythonanywhere.sh
```

Lo script guiderà attraverso molti dei passaggi sopra descritti, ma alcune configurazioni manuali saranno ancora necessarie.
