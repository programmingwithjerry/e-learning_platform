# Import all necessary settings and configurations from the base settings module.
from .base import *

# Disable debug mode for production to ensure sensitive information is not exposed in error pages.
DEBUG = False

# Define a list of admin users to receive error notifications. Each entry contains a name and an email address.
ADMINS = [
    ('Antonio M', 'email@mydomain.com'),
]

# Define the list of hosts/domain names that this Django site can serve.
# The wildcard '*' allows any host, but for production, it's better to restrict this to specific domains.
ALLOWED_HOSTS = ['*']

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
