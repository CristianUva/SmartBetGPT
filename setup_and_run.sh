# !/bin/bash
# chmod +x setup_and_run.sh
# ./setup_and_run.sh

echo "===== Installazione e avvio di PaginaRegistrazione ====="

echo "Creazione dell'ambiente virtuale..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Errore nella creazione dell'ambiente virtuale!"
    echo "Assicurati che Python sia installato correttamente."
    echo "Potrebbe essere necessario installare il pacchetto python3-venv."
    echo "Su Ubuntu/Debian: sudo apt install python3-venv"
    exit 1
fi

echo "Attivazione dell'ambiente virtuale..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Errore nell'attivazione dell'ambiente virtuale!"
    exit 1
fi

echo "Installazione delle dipendenze..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Errore nell'installazione delle dipendenze!"
    exit 1
fi

echo "Creazione del database..."
python create_db.py
if [ $? -ne 0 ]; then
    echo "Errore nella creazione del database!"
    exit 1
fi

echo "===== Avvio dell'applicazione ====="
echo "L'applicazione sta partendo su http://localhost:5000"
echo "Premi CTRL+C per terminare l'applicazione"
python app.py
