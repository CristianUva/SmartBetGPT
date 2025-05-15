# Script to update database structure
from app import app, db
from models.user import User
from flask_migrate import Migrate

# Create migration instance
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # This will detect model changes and update the database
        db.create_all()
        print("Database updated successfully.")
