# routes/api_routes.py
from flask import Blueprint, jsonify, request
from flask_login import login_required
from services.match_service import MatchService
from services.football_service import FootballService

# Create blueprints
api = Blueprint('api', __name__)

# Initialize services
match_service = MatchService()
football_service = FootballService()

@api.route('/api/competitions')
@login_required
def api_competitions():
    """API endpoint to get the list of competitions"""
    competitions = match_service.get_available_competitions()
    return jsonify(competitions)

@api.route('/api/matches/upcoming')
@login_required
def api_upcoming_matches():
    """API endpoint to get upcoming matches"""
    days = request.args.get('days', default=3, type=int)
    timezone = request.args.get('timezone', default='Europe/Rome', type=str)
    competitions = request.args.getlist('competitions')
    
    matches = match_service.get_upcoming_matches(
        days=days,
        competitions=competitions if competitions else None,
        timezone=timezone
    )
    
    return jsonify(matches)

@api.route('/api/matches/finished')
@login_required
def api_finished_matches():
    """API endpoint to get finished matches"""
    days = request.args.get('days', default=7, type=int)
    timezone = request.args.get('timezone', default='Europe/Rome', type=str)
    competitions = request.args.getlist('competitions')
    
    matches = match_service.get_finished_matches(
        days=days,
        competitions=competitions if competitions else None,
        timezone=timezone
    )
    
    return jsonify(matches)

@api.route('/api/football/upcoming-matches', methods=['GET'])
@login_required
def api_football_upcoming_matches():
    """API endpoint to get upcoming football matches"""
    days = request.args.get('days', default=7, type=int)
    matches_data = football_service.get_upcoming_matches(days=days)
    
    if not matches_data:
        return jsonify({"error": "Impossibile recuperare i dati delle partite"}), 500
    
    return jsonify(matches_data)

@api.route('/api/football/standings/<int:competition_id>', methods=['GET'])
@login_required
def api_football_standings(competition_id):
    """API endpoint to get standings for a competition"""
    standings_data = football_service.get_standings(competition_id)
    
    if not standings_data:
        return jsonify({"error": "Impossibile recuperare la classifica"}), 500
    
    return jsonify(standings_data)
