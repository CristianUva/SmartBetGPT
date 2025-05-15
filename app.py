# app.py - Main application file
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    """Create and configure the Flask application"""
    # Initialize Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Create instance folder if it doesn't exist
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Load configuration
    configure_app(app)
    
    # Initialize extensions with the app
    init_extensions(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Initialize database models
    init_models()
    
    return app

def configure_app(app):
    """Configure the Flask application"""
    # Check if we're on PythonAnywhere
    is_pythonanywhere = 'PYTHONANYWHERE_SITE' in os.environ
    
    # Configure database based on environment
    if is_pythonanywhere:
        # MySQL configuration for PythonAnywhere
        mysql_user = os.environ.get('MYSQL_USER', 'SmartBetGPT')
        mysql_password = os.environ.get('MYSQL_PASSWORD', 'Angelogalanti69')
        mysql_host = os.environ.get('MYSQL_HOST', 'SmartBetGPT.mysql.pythonanywhere-services.com')
        mysql_db = os.environ.get('MYSQL_DATABASE', 'SmartBetGPT$database')
        
        # MySQLdb URL format
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
        app.logger.info(f"Configurato il database MySQL su PythonAnywhere: {mysql_host}")
    else:
        # Local configuration - still supporting both SQLite and MySQL
        if os.environ.get('USE_MYSQL_LOCAL', 'false').lower() == 'true':
            # Use MySQL locally too
            mysql_user = os.environ.get('MYSQL_USER_LOCAL', 'root')
            mysql_password = os.environ.get('MYSQL_PASSWORD_LOCAL', 'x')
            mysql_host = os.environ.get('MYSQL_HOST_LOCAL', 'localhost')
            mysql_db = os.environ.get('MYSQL_DATABASE_LOCAL', 'smartbetgpt')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
            app.logger.info(f"Configurato il database MySQL locale: {mysql_host}")
        else:
            # Default to SQLite for local development
            basedir = os.path.abspath(os.path.dirname(__file__))
            db_path = os.path.join(basedir, 'database.db')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
            app.logger.info(f"Configurato database SQLite locale: {db_path}")
    
    # App configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

def init_extensions(app):
    """Initialize Flask extensions"""
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Per favore effettua il login per accedere a questa pagina.'
    
    # Initialize Flask-Mail
    mail.init_app(app)

def register_error_handlers(app):
    """Register error handlers"""
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    @app.context_processor
    def inject_now():
        """Add 'now' variable to all templates"""
        return {'now': datetime.utcnow()}

def register_blueprints(app):
    """Register blueprints"""
    # Import blueprints
    from routes.main_routes import main
    from routes.auth_routes import auth
    from routes.match_routes import match
    from routes.chatbot_routes import chatbot
    from routes.api_routes import api
    
    # Initialize database in routes where needed
    from routes.auth_routes import init_routes as init_auth_routes
    init_auth_routes(db)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(match)
    app.register_blueprint(chatbot)
    app.register_blueprint(api)

def init_models():
    """Initialize database models"""
    # Import and initialize models
    from models.user import init_db as init_user_db
    init_user_db(db)
    
    # Setup user loader
    from models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

# Create the application
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
