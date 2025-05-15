# Altre configurazioni dell'applicazione
import os
from datetime import timedelta

# La configurazione del database è ora in app.py
# Compatibile sia con SQLite (locale) che con MySQL (PythonAnywhere)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Chiave segreta per la sicurezza
SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key')

# Configurazione sessione
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# Configurazione email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('EMAIL_USER')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')

# Configurazioni per le funzionalità di scommesse
DEFAULT_COMPETITIONS = ['2021', '2014', '2019', '2002', '2015']  # IDs per Premier League, La Liga, Serie A, Bundesliga, Ligue 1