import os

PROJECT_NAME = 'flask_rest'

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "qwwAAFXAE4534GDFSEVVBE565as321dsewf"

# Secret key for signing cookies
SECRET_KEY = "Sfkjmvert3fgjne,43!k3l2&k3hksjh%m,hw"

MONGODB_SETTINGS = {
    'DB': '',
    'USERNAME': '',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': 27017
}

MEDIA = '/media/'
MEDIA_PATH = os.path.join(BASE_DIR, 'media')

STATIC = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, 'static')

APPS = [

]
