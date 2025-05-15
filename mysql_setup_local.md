# Configurazione MySQL locale

Questo documento spiega come configurare e utilizzare MySQL per lo sviluppo locale di SmartBetGPT.

## 1. Installazione di MySQL

### Per Windows:

1. Scarica MySQL Installer da [MySQL Download](https://dev.mysql.com/downloads/installer/)
2. Esegui l'installer e scegli "Developer Default"
3. Segui le istruzioni per l'installazione
4. Imposta una password per l'utente root

### Per macOS:

```bash
brew install mysql
brew services start mysql
```

### Per Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

## 2. Crea un database per l'applicazione

Accedi al server MySQL:

```bash
mysql -u root -p
```

Crea un database e un utente per l'applicazione:

```sql
CREATE DATABASE smartbetgpt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'smartbetgpt'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON smartbetgpt.* TO 'smartbetgpt'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 3. Configurazione delle variabili d'ambiente

Copia il file `.env.example` in `.env`:

```bash
cp .env.example .env
```

Modifica il file `.env` con i valori appropriati:

```
USE_MYSQL_LOCAL=true
MYSQL_USER_LOCAL=smartbetgpt
MYSQL_PASSWORD_LOCAL=password
MYSQL_HOST_LOCAL=localhost
MYSQL_DATABASE_LOCAL=smartbetgpt
```

## 4. Installazione dei pacchetti Python necessari

```bash
pip install -r requirements.txt
```

## 5. Inizializzazione del database

Esegui lo script di creazione del database:

```bash
python create_db.py
```

## 6. Test della connessione al database

```bash
python test_mysql_connection.py
```

## 7. Eseguire l'applicazione

```bash
python __main__.py
```

## Risoluzione dei problemi

### Errore di connessione al database

Se riscontri errori di connessione, verifica:

1. Che il server MySQL sia in esecuzione
2. Che le credenziali nel file `.env` siano corrette
3. Che il database sia stato creato correttamente

### Errori di permesso

Se riscontri errori di permesso, verifica i privilegi dell'utente del database:

```bash
mysql -u root -p
```

```sql
SHOW GRANTS FOR 'smartbetgpt'@'localhost';
```

### Migrazione da SQLite

Se vuoi migrare dati da un database SQLite esistente a MySQL:

```bash
python migrate_to_mysql.py
```
