# services/openrouter_service.py
import os
import logging
import requests
from flask import current_app

class OpenRouterService:
    """Service to handle OpenRouter API interactions for AI chatbot functionality"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Definizione del comportamento dell'AI - modifica questa variabile per personalizzare l'AI
        self.system_message = (
            "Sei un'AI esperta di scommesse calcistiche con accesso a dati in tempo reale da Football-data.org. "
            "Il tuo compito è analizzare dati calcistici (campionati, squadre, partite, classifiche, statistiche) "
            "e fornire pronostici quantitativi e standardizzati. Ogni output deve includere: squadre coinvolte; tipo di scommessa (esito, gol, handicap, ecc.); probabilità stimata; quota consigliata; breve motivazione tecnica basata sui dati fattuali (1–2 frasi).\n"
            "Se la richiesta è generica o poco chiara, scegli una partita o un evento calcistico rilevante e fornisci comunque un esempio concreto di pronostico, spiegando brevemente la scelta. Non chiedere ulteriori dettagli all'utente, ma proponi direttamente un'analisi o un pronostico reale e attuale.\n"
            "Non rispondere mai con messaggi generici o istruzioni su come chiedere, ma fornisci sempre una risposta calcistica specifica, anche se devi scegliere tu la partita o il campionato.\n"
            "Hai accesso a dati reali da Football-data.org. Quando un utente chiede informazioni su partite, classifiche o statistiche, userai questi dati aggiornati per la tua analisi.\n"
            "\n"
            "VINCOLI:\n"
            "1. Ambito ristretto: rispondi solo a pronostici calcistici. Se l'input non è pertinente, rispondi comunque con un esempio di pronostico calcistico reale.\n"
            "2. Divieti: non fornire consulenze finanziarie, legali o di gioco illecito; non suggerire partite truccate o metodi illegali.\n"
            "3. Privacy: non memorizzare o richiedere dati personali; rispetta GDPR.\n"
            "4. Tono: professionale e oggettivo; usa linguaggio basato su probabilità e rischi; evita promesse di vittoria certa.\n"
            "5. Nessuna opinione personale, gossip o contenuti extra non rilevanti; brevi avvertenze sul rischio del gioco sono ammesse, ma evitare lunghi disclaimer legali."
        )
        
        # Lista dei modelli disponibili (focus su modelli gratuiti o con free tier)
        self.available_models = [
            {"id": "deepseek/deepseek-chat-v3-0324:free", "name": "DeepSeek Chat V3 (Free Tier)"},
            #Questi sono inseriti come esempio, puoi aggiungere altri modelli gratuiti, 
            {"id": "anthropic/claude-instant-1.1", "name": "Claude (PREMIUM NECESSARIO))"},
            {"id": "google/gemini-2.5-pro-exp-03-25", "name": "Gemini (PREMIUM NECESSARIO)"},
            {"id": "meta-llama/llama-2-13b-chat", "name": "Llama 2 13B (PREMIUM NECESSARIO)"},
            {"id": "mistralai/mistral-7b", "name": "Mistral 7B (PREMIUM NECESSARIO)"}
        ]
        
        # Default model
        self.default_model = "deepseek/deepseek-chat-v3-0324:free"
        
        # Dizionario per memorizzare temporaneamente le conversazioni attive
        self.conversation_history = {}
    
    def get_api_key(self):
        """Get the API key"""
        return self.api_key
    
    def get_available_models(self):
        """Get the list of available models"""
        return self.available_models
    
    def get_default_model(self):
        """Get the default model"""
        return self.default_model
    
    def get_system_message(self):
        """Get the system message for AI instructions"""
        return self.system_message
    
    def get_user_conversation_history(self, user_id):
        """Get or initialize the conversation history for a user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def add_to_conversation_history(self, user_id, role, content):
        """Add a message to the conversation history"""
        history = self.get_user_conversation_history(user_id)
        history.append({"role": role, "content": content})
        # Mantieni solo gli ultimi 20 messaggi per non appesantire troppo il contesto
        if len(history) > 20:
            history.pop(0)  # Rimuovi il messaggio più vecchio
    
    def generate_response(self, user_id, user_message, selected_model=None, football_data=None):
        """Generate a response from OpenRouter AI"""
        if not selected_model:
            selected_model = self.default_model
        
        # Validazione
        valid_model_ids = [model["id"] for model in self.available_models]
        if selected_model not in valid_model_ids:
            selected_model = self.default_model
        
        # Aggiungi il messaggio dell'utente alla cronologia
        self.add_to_conversation_history(user_id, "user", user_message)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Aggiungi il messaggio di sistema e la cronologia delle conversazioni
        messages = [{"role": "system", "content": self.system_message}]
        
        # Recupera la cronologia delle conversazioni dell'utente
        conversation_history_user = self.get_user_conversation_history(user_id)
        
        # Aggiungi eventuali dati calcistici alla conversazione
        if football_data:
            import json
            football_data_str = json.dumps(football_data, indent=2)
            messages.append({
                "role": "system", 
                "content": f"Ecco i dati calcistici rilevanti per la richiesta dell'utente:\n{football_data_str}\nUsa questi dati per fornire una risposta accurata."
            })
        
        # Aggiungi la cronologia delle conversazioni al messaggio
        for msg in conversation_history_user:
            if msg["role"] != "system":  # Evita di inserire messaggi di sistema che potrebbero confondere il modello
                messages.append(msg)
        
        payload = {
            "model": selected_model,
            "messages": messages
        }
        
        # Se non è configurata la chiave API di OpenRouter, usa una risposta simulata
        if not self.api_key:
            logging.warning("OpenRouter API key non configurata o token esauriti")
            simulated_response = "La chiave API del chatbot non è configurata o i token sono esauriti. Contatta l'amministratore per assistenza."
            
            # Aggiungi anche la risposta simulata alla cronologia
            self.add_to_conversation_history(user_id, "assistant", simulated_response)
            
            return simulated_response, "Simulazione (API Key non configurata)"
        
        try:
            logging.info(f"Sending request to OpenRouter API with model: {selected_model}")
            logging.info(f"API URL: {self.api_url}")
            logging.info(f"Headers: {headers}")
            logging.info(f"Payload: {payload}")
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response headers: {response.headers}")
            
            if response.status_code != 200:
                logging.error(f"API returned status {response.status_code}: {response.text}")
                error_message = f"API OpenRouter errore {response.status_code}: {response.text}"
                return error_message, selected_model
            
            response.raise_for_status()
            response_data = response.json()
            logging.info(f"Response data: {response_data}")
            
            ai_response = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Aggiungi la risposta dell'AI alla cronologia
            self.add_to_conversation_history(user_id, "assistant", ai_response)
            
            return ai_response, selected_model
        except requests.exceptions.Timeout:
            error_message = "Timeout nell'API OpenRouter - riprova più tardi"
            logging.error(error_message)
            return error_message, selected_model
        except requests.exceptions.ConnectionError:
            error_message = "Errore di connessione all'API OpenRouter"
            logging.error(error_message)
            return error_message, selected_model
        except Exception as e:
            error_message = f"Errore nell'API OpenRouter: {str(e)}"
            logging.error(error_message)
            return error_message, selected_model
