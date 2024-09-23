import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask configurations
DEBUG = True  # Enable debug mode (set to False in production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')  # Secret key for sessions

# Database configurations (SQLite)
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'store.sqlite3')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable the overhead of tracking modifications
