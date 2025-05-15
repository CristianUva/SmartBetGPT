import requests
import logging
from datetime import datetime, timedelta
import pytz
from collections import defaultdict
import os
import json
from dotenv import load_dotenv

# Configurazione per Football-Data.org
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

class MatchService:
    """Service to handle match-related operations"""
    
    def __init__(self):
        self.api_url = "https://api.football-data.org/v4/matches"
        self.headers = {'X-Auth-Token': API_KEY}
        self.matches_cache = {}  # Cache to store fetched matches
        self.cache_timestamp = None
        self.cache_ttl = 1800  # Cache TTL in seconds (30 minutes)
        # In-memory competition cache
        self.competitions_cache = None
    
    def get_upcoming_matches(self, days=3, competitions=None, timezone='UTC'):
        """
        Get upcoming matches for the specified number of days
        
        Args:
            days: Number of days to look ahead
            competitions: List of competition IDs to filter by
            timezone: User's timezone for date display
            
        Returns:
            List of match objects
        """
        # Check cache first
        cache_key = f"upcoming_{days}_{'-'.join(competitions) if competitions else 'all'}"
        if cache_key in self.matches_cache and self.cache_timestamp and \
           (datetime.now() - self.cache_timestamp).total_seconds() < self.cache_ttl:
            logging.info(f"Using cached matches for {cache_key}")
            return self.matches_cache[cache_key]
        
        # Calculate date range
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        
        # Format dates for API
        date_from = today.strftime("%Y-%m-%d")
        date_to = end_date.strftime("%Y-%m-%d")
        
        # Prepare parameters
        params = {
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        
        # Add competitions filter if provided
        if competitions:
            params["competitions"] = ",".join(competitions)
        
        try:
            # Make API request
            response = requests.get(self.api_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            # Process matches
            matches = response.json().get("matches", [])
            
            # Convert dates to user timezone
            tz = pytz.timezone(timezone)
            for match in matches:
                if "utcDate" in match:
                    utc_date = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
                    # Formato italiano: giorno/mese/anno ore:minuti
                    match["localDate"] = utc_date.astimezone(tz).strftime("%d/%m/%Y %H:%M")
            
            # Update cache
            self.matches_cache[cache_key] = matches
            self.cache_timestamp = datetime.now()
            
            return matches
            
        except Exception as e:
            logging.error(f"Error fetching upcoming matches: {e}")
            return []
    
    def get_match_by_id(self, match_id):
        """
        Get details for a specific match by ID
        
        Args:
            match_id: The ID of the match to fetch
            
        Returns:
            Match object or None if not found
        """
        # Check all cached matches
        for cache_key, matches in self.matches_cache.items():
            for match in matches:
                if str(match.get("id")) == str(match_id):
                    return match
        
        # If not in cache, fetch from API
        try:
            url = f"https://api.football-data.org/v4/matches/{match_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching match {match_id}: {e}")
            return None
    
    def get_available_competitions(self):
        """
        Get list of available competitions
        
        Returns:
            List of competition objects with id, name, and code
        """
        # Use cache if available
        if self.competitions_cache:
            return self.competitions_cache
        
        try:
            url = "https://api.football-data.org/v4/competitions"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            competitions = response.json().get("competitions", [])
            
            # Process and filter competitions
            result = []
            for comp in competitions:
                if comp.get("type") == "LEAGUE":  # Only include leagues
                    result.append({
                        "id": comp.get("id"),
                        "name": comp.get("name"),
                        "code": comp.get("code"),
                        "country": comp.get("area", {}).get("name")
                    })
            
            # Sort by country and name
            result.sort(key=lambda x: (x.get("country", ""), x.get("name", "")))
            
            # Update cache
            self.competitions_cache = result
            return result
            
        except Exception as e:
            logging.error(f"Error fetching competitions: {e}")
            return []
    
    def group_matches_by_date(self, matches, timezone='UTC'):
        """
        Group matches by date for display
        
        Args:
            matches: List of match objects
            timezone: User's timezone for date display
            
        Returns:
            Dictionary with dates as keys and lists of matches as values
        """
        grouped = defaultdict(list)
        
        for match in matches:
            if "utcDate" in match:
                # Convert UTC date to user timezone
                utc_date = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
                user_date = utc_date.astimezone(pytz.timezone(timezone))
                date_key = user_date.strftime("%Y-%m-%d")
                
                # Format date for display
                today = datetime.now(pytz.timezone(timezone)).date()
                match_date = user_date.date()
                
                if match_date == today:
                    display_date = "Today"
                elif match_date == today + timedelta(days=1):
                    display_date = "Tomorrow"
                else:
                    display_date = user_date.strftime("%A, %d %B")
                
                if date_key not in grouped:
                    grouped[date_key] = {
                        "display_date": display_date,
                        "matches": []
                    }
                
                grouped[date_key]["matches"].append(match)
        
        # Sort matches within each day by time
        for date_key in grouped:
            grouped[date_key]["matches"].sort(key=lambda m: m.get("utcDate", ""))
        
        # Convert to sorted list of date groups
        result = [{"date": k, **v} for k, v in sorted(grouped.items())]
        
        return result
    
    def get_finished_matches(self, days=7, competitions=None, timezone='UTC'):
        """
        Ottiene le partite terminate negli ultimi giorni specificati
        
        Args:
            days: Numero di giorni nel passato da considerare
            competitions: Lista di ID di competizioni da filtrare
            timezone: Fuso orario dell'utente per la visualizzazione delle date
            
        Returns:
            Lista di match terminati
        """
        # Calcola l'intervallo di date nel passato
        today = datetime.now().date()
        start_date = today - timedelta(days=days)
        
        try:
            # Prepara i parametri per la chiamata API
            params = {
                "status": "FINISHED",
                "dateFrom": start_date.strftime("%Y-%m-%d"),
                "dateTo": today.strftime("%Y-%m-%d")
            }
            
            # Aggiungi filtro competizioni se fornito
            if competitions:
                params["competitions"] = ",".join(competitions)
            
            # Esegui la chiamata API
            response = requests.get(self.api_url, headers=self.headers, params=params)
            response.raise_for_status()
            matches = response.json().get("matches", [])
            
            # Converti le date nel fuso orario dell'utente
            tz = pytz.timezone(timezone)
            for match in matches:
                if "utcDate" in match:
                    utc_date = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
                    # Formato italiano: giorno/mese/anno ore:minuti
                    match["localDate"] = utc_date.astimezone(tz).strftime("%d/%m/%Y %H:%M")
            
            # Ordina le partite per data (più recenti prima)
            matches.sort(key=lambda m: m.get("utcDate", ""), reverse=True)
            
            return matches
            
        except Exception as e:
            logging.error(f"Error fetching finished matches: {e}")
            return []