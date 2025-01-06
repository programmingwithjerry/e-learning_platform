# Import all necessary settings and configurations from the base settings module.
from .base import *

# Enable debug mode. Set this to False in production for better security and performance.
DEBUG = True

# Configure the database settings. The default database is SQLite.
DATABASES = {
    'default': {
        # Specify the database engine to use. In this case, it's SQLite.
        'ENGINE': 'django.db.backends.sqlite3',
        # Define the path to the SQLite database file.
        # BASE_DIR is assumed to be the project's root directory.
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
