# routes/match_routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from services.match_service import MatchService

# Create blueprint
match = Blueprint('match', __name__)

# Initialize service
match_service = MatchService()

@match.route('/matches')
@login_required
def matches():
    """Display upcoming matches"""
    # Recupera i parametri di query opzionali
    days = request.args.get('days', default=3, type=int)
    timezone = request.args.get('timezone', default='Europe/Rome', type=str)
    competitions = request.args.getlist('competitions')
    
    # Ottiene le partite imminenti dal servizio
    matches_data = match_service.get_upcoming_matches(
        days=days, 
        competitions=competitions if competitions else None,
        timezone=timezone
    )
    
    # Raggruppa le partite per data per una migliore visualizzazione
    grouped_matches = match_service.group_matches_by_date(matches_data, timezone)
    
    # Recupera le competizioni disponibili per il filtro
    competitions_data = match_service.get_available_competitions()
    
    return render_template(
        'matches.html', 
        grouped_matches=grouped_matches,
        competitions=competitions_data,
        selected_competitions=competitions,
        days=days,
        timezone=timezone
    )

@match.route('/match/<int:match_id>')
@login_required
def match_details(match_id):
    """Display details for a specific match"""
    # Recupera i dettagli della partita specifica
    match_data = match_service.get_match_by_id(match_id)
    
    if not match_data:
        flash('Partita non trovata', 'danger')
        return redirect(url_for('match.matches'))
    
    return render_template('match_details.html', match=match_data)

@match.route('/statistics')
@login_required
def statistics():
    """Display match statistics"""
    # Recupera i parametri di query opzionali
    days = request.args.get('days', default=7, type=int)
    timezone = request.args.get('timezone', default='Europe/Rome', type=str)
    competitions = request.args.getlist('competitions')
    
    # Ottiene le partite terminate recentemente
    finished_matches = match_service.get_finished_matches(
        days=days,
        competitions=competitions if competitions else None,
        timezone=timezone
    )
    
    # Raggruppa le partite per data
    grouped_matches = match_service.group_matches_by_date(finished_matches, timezone)
    
    # Recupera le competizioni disponibili per il filtro
    competitions_data = match_service.get_available_competitions()
    
    return render_template(
        'statistics.html',
        grouped_matches=grouped_matches,
        competitions=competitions_data,
        selected_competitions=competitions,
        days=days,
        timezone=timezone
    )
