import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Team:
    """Model representing a football team"""
    id: str
    name: str
    code: str = None
    country: str = None
    logo: str = None
    
    # Additional fields for stats
    form: str = None  # Recent form (e.g., WWDLL)
    
    def __post_init__(self):
        if not self.code and self.name:
            # Generate a code if not provided
            self.code = self.name[:3].upper()

@dataclass
class Competition:
    """Model representing a football competition/league"""
    id: str
    name: str
    code: str = None
    country: str = None
    logo: str = None
    
    def __post_init__(self):
        if not self.code and self.name:
            # Generate a code if not provided
            self.code = self.name[:3].upper()

@dataclass
class Odds:
    """Model representing match odds from a bookmaker"""
    name: str  # Bookmaker name
    home_win: str
    draw: str
    away_win: str
    over_under: Dict[str, Dict[str, str]] = field(default_factory=dict)
    both_teams_to_score: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        # Convert string odds to float for internal use
        self.home_win_float = float(self.home_win) if self.home_win else None
        self.draw_float = float(self.draw) if self.draw else None
        self.away_win_float = float(self.away_win) if self.away_win else None

@dataclass
class Match:
    """Model representing a football match with all related data"""
    id: str
    home_team: Team
    away_team: Team
    utc_date: datetime.datetime
    status: str = "SCHEDULED"  # SCHEDULED, LIVE, FINISHED, POSTPONED, CANCELED
    competition: Optional[Competition] = None
    venue: str = None
    matchday: int = None
    score: Dict[str, Any] = field(default_factory=dict)
    odds: List[Dict[str, Any]] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_finished(self) -> bool:
        """Check if the match is finished"""
        return self.status == "FINISHED"
    
    @property
    def is_upcoming(self) -> bool:
        """Check if the match is upcoming"""
        return self.status == "SCHEDULED" and self.utc_date > datetime.datetime.utcnow()
    
    @property
    def is_live(self) -> bool:
        """Check if the match is live"""
        return self.status == "LIVE"
    
    @property
    def formatted_date(self) -> str:
        """Return a formatted date string"""
        if not self.utc_date:
            return "TBD"
        # Convert UTC to local time
        local_date = self.utc_date.replace(tzinfo=datetime.timezone.utc).astimezone()
        return local_date.strftime("%d %b %Y %H:%M")
    
    @property 
    def short_date(self) -> str:
        """Return a short date string (e.g., "Today 15:00")"""
        if not self.utc_date:
            return "TBD"
        
        # Convert UTC to local time
        local_date = self.utc_date.replace(tzinfo=datetime.timezone.utc).astimezone()
        today = datetime.datetime.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        
        if local_date.date() == today:
            prefix = "Today"
        elif local_date.date() == tomorrow:
            prefix = "Tomorrow"
        else:
            # For other dates, use the short date format
            return local_date.strftime("%d %b %H:%M")
            
        return f"{prefix} {local_date.strftime('%H:%M')}"
    
    def get_best_odds(self, outcome: str) -> float:
        """
        Get the best (highest) odds for a specific outcome
        
        Args:
            outcome: One of 'home_win', 'draw', 'away_win'
        
        Returns:
            The highest odds value, or None if no odds available
        """
        if not self.odds:
            return None
            
        best_value = 0.0
        
        for odd in self.odds:
            if outcome in odd and odd[outcome]:
                try:
                    value = float(odd[outcome])
                    best_value = max(best_value, value)
                except (ValueError, TypeError):
                    pass
                    
        return best_value if best_value > 0 else None