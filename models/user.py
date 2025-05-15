# models/user.py
from datetime import datetime, timedelta
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer
from flask import current_app
import secrets

# Database instance will be initialized in app.py and imported here
db = None
User = None

def init_db(app_db):
    """Initialize database instance from app.py"""
    global db, User
    db = app_db
    
    # Define the User model only after db is initialized
    class UserModel(UserMixin, db.Model):
        """Model representing a user in the system"""
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        name = db.Column(db.String(100), nullable=False)
        created_on = db.Column(db.DateTime, default=datetime.utcnow)
        email_confirmed = db.Column(db.Boolean, default=False)
        email_confirmed_on = db.Column(db.DateTime, nullable=True)
        reset_token = db.Column(db.String(100), unique=True, nullable=True)
        reset_token_expiry = db.Column(db.DateTime, nullable=True)
        
        def get_reset_token(self):
            """Generate a reset token for password reset"""
            token = secrets.token_urlsafe(32)
            self.reset_token = token
            self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            return token
            
        def verify_reset_token(self, token):
            """Verify a reset token is valid"""
            if self.reset_token != token:
                return False
                
            if datetime.utcnow() > self.reset_token_expiry:
                return False
                
            return True
            
        def clear_reset_token(self):
            """Clear reset token after use"""
            self.reset_token = None
            self.reset_token_expiry = None
            db.session.commit()
        
        def get_confirmation_token(self):
            """Generate a token for email confirmation"""
            s = Serializer(current_app.config['SECRET_KEY'])
            return s.dumps({'user_id': self.id})
            
        @staticmethod
        def verify_confirmation_token(token):
            """Verify an email confirmation token"""
            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                user_id = s.loads(token)['user_id']
            except:
                return None
            return User.query.get(user_id)
    
    User = UserModel
