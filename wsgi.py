#!/usr/bin/env python3
"""
WSGI entry point for production deployment
This file is used by Gunicorn to serve the application
"""

import os
import sys

# Add the project directory to the Python path
project_home = '/var/www/smartbetgpt'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
