# routes/chatbot_routes.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.openrouter_service import OpenRouterService
from services.football_service import FootballService

# Create blueprint
chatbot = Blueprint('chatbot', __name__)

# Initialize services
openrouter_service = OpenRouterService()
football_service = FootballService()

@chatbot.route('/chatbot')
@login_required
def chatbot_page():
    """Chatbot interface page"""
    # Passa i modelli disponibili al template per il selettore
    return render_template(
        'chatbot.html', 
        models=openrouter_service.get_available_models(), 
        default_model=openrouter_service.get_default_model()
    )

@chatbot.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """API endpoint for chat interactions"""
    data = request.json
    user_message = data.get('message', '')
    selected_model = data.get('model', openrouter_service.get_default_model())
    
    # Validazione
    if not user_message:
        return jsonify({"error": "Messaggio non fornito"}), 400
    
    # Ottieni l'ID utente per la conversazione
    user_id = current_user.id
    
    # Determina se è necessario recuperare dati calcistici basati sul messaggio dell'utente
    football_data = {}
    
    # Se l'utente chiede info su partite imminenti
    if any(keyword in user_message.lower() for keyword in ["prossime partite", "partite di oggi", "partite future", "calendario"]):
        matches_data = football_service.get_upcoming_matches(days=7)
        if matches_data:
            football_data["upcoming_matches"] = matches_data
    
    # Se l'utente chiede informazioni su classifiche
    if any(keyword in user_message.lower() for keyword in ["classifica", "standings", "posizione"]):
        # Cerca di capire quale competizione
        for comp in football_service.get_popular_competitions():
            if comp["name"].lower() in user_message.lower():
                standings_data = football_service.get_standings(comp['id'])
                if standings_data:
                    football_data["standings"] = standings_data
                break
    
    # Genera la risposta tramite il servizio OpenRouter
    ai_response, used_model = openrouter_service.generate_response(
        user_id, 
        user_message, 
        selected_model,
        football_data
    )
    
    return jsonify({"response": ai_response, "model": used_model})
