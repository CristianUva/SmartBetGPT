# create_db.py - Database initialization script
import os
import sqlite3
from app import app, db
from models.user import User

print("Inizializzazione database...")

with app.app_context():
    try:
        # Ensure the database file exists
        db_path = os.path.join(app.instance_path, 'database.db')
        print(f"Percorso database: {db_path}")
        
        # Create the database file if it doesn't exist
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            print("Database SQLite creato con successo")
            conn.close()
        
        # Create all tables defined in models
        db.create_all()
        print("Tabelle create con successo nel database")
        
        # You can add initial data here if needed
        
    except Exception as e:
        print(f"Errore durante l'inizializzazione del database: {str(e)}")

print("Processo completato.")
