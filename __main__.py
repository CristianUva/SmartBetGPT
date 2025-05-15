# __main__.py
"""Entry point for the application."""
from app import create_app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
