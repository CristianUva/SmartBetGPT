@echo off
echo ===== Installazione e avvio di PaginaRegistrazione =====

echo Creazione dell'ambiente virtuale...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Errore nella creazione dell'ambiente virtuale!
    echo Assicurati che Python sia installato e disponibile nel PATH.
    pause
    exit /b 1
)

echo Attivazione dell'ambiente virtuale...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Errore nell'attivazione dell'ambiente virtuale!
    pause
    exit /b 1
)

echo Installazione delle dipendenze...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Errore nell'installazione delle dipendenze!
    pause
    exit /b 1
)

echo Creazione del database...
python create_db.py
if %ERRORLEVEL% NEQ 0 (
    echo Errore nella creazione del database!
    pause
    exit /b 1
)

echo ===== Avvio dell'applicazione =====
echo L'applicazione sta partendo su http://localhost:5000
echo Premi CTRL+C per terminare l'applicazione
python app.py

pause
