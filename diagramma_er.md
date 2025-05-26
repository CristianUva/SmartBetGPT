erDiagram
    %% Entità User - L'unica tabella del database attualmente definita
    User {
        int id PK "PRIMARY KEY"
        string email UK "UNIQUE, NOT NULL, VARCHAR(100)"
        string password "NOT NULL, VARCHAR(200)"
        string name "NOT NULL, VARCHAR(100)"
        datetime created_on "DEFAULT datetime.utcnow"
        boolean email_confirmed "DEFAULT FALSE"
        datetime email_confirmed_on "NULLABLE"
        string reset_token "UNIQUE, NULLABLE, VARCHAR(100)"
        datetime reset_token_expiry "NULLABLE"
    }

    %% Note: I dati delle partite e delle API vengono gestiti in memoria
    %% tramite i servizi ma non sono persistiti nel database
    
    %% Entità virtuali (gestite via API, non nel database)
    FootballData {
        string note "Dati gestiti via API Football-data.org"
        string competitions "Non persistiti nel database"
        string matches "Caricati dinamicamente"
        string standings "Via servizi esterni"
    }

    ChatData {
        string note "Conversazioni gestite in memoria"
        string conversation_history "Non persistite nel database"
        string openrouter_responses "Temporanee per sessione"
    }

    %% Relazioni concettuali (non nel database)
    User ||--o{ FootballData : "accesses via API"
    User ||--o{ ChatData : "interacts with chatbot"