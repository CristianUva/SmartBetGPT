# services/football_service.py
import os
import requests
import logging
from datetime import datetime, timedelta
import json

class FootballService:
    """Service to handle football data from football-data.org API"""
    
    def __init__(self):
        self.api_key = os.getenv('FOOTBALL_API_KEY', 'd9cd4e4ddc5047f98e5d8ab1b89a4820')
        self.api_base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': self.api_key}
        
        # Lista di competizioni disponibili per riferimento rapido
        self.popular_competitions = [
            {"id": 2001, "name": "Champions League"},
            {"id": 2021, "name": "Premier League"},
            {"id": 2014, "name": "La Liga"},
            {"id": 2019, "name": "Serie A"},
            {"id": 2002, "name": "Bundesliga"},
            {"id": 2015, "name": "Ligue 1"}
        ]
    
    def get_popular_competitions(self):
        """Get the list of popular competitions"""
        return self.popular_competitions
    
    def get_football_data(self, endpoint, params=None):
        """
        Get data from football-data.org API
        
        Args:
            endpoint: API endpoint (can be relative path)
            params: Query parameters
            
        Returns:
            JSON response or None if error
        """
        # Ensure endpoint starts with BASE_URL
        if not endpoint.startswith(self.api_base_url):
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint
            endpoint = f"{self.api_base_url}{endpoint}"
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Errore API football-data.org: {e}")
            return None
    
    def get_upcoming_matches(self, days=3):
        """
        Get upcoming matches for the next X days
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of matches or empty list if error
        """
        from datetime import datetime
        
        today = datetime.today().strftime('%Y-%m-%d')
        next_days = (datetime.today() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        endpoint = f"{self.api_base_url}/matches"
        params = {
            'dateFrom': today,
            'dateTo': next_days
        }
        
        return self.get_football_data(endpoint, params)
    
    def get_match_by_id(self, match_id):
        """
        Get details for a specific match
        
        Args:
            match_id: ID of the match
            
        Returns:
            Match details or None if not found
        """
        endpoint = f"{self.api_base_url}/matches/{match_id}"
        return self.get_football_data(endpoint)
    
    def get_standings(self, competition_id):
        """
        Get standings for a specific competition
        
        Args:
            competition_id: ID of the competition
            
        Returns:
            Standings data or None if error
        """
        endpoint = f"{self.api_base_url}/competitions/{competition_id}/standings"
        return self.get_football_data(endpoint)
    
    def get_competitions(self):
        """
        Get all available competitions
        
        Returns:
            List of competitions or None if error
        """
        endpoint = f"{self.api_base_url}/competitions"
        return self.get_football_data(endpoint)
