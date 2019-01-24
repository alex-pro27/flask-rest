import os

PROJECT_NAME = 'example'

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
CSRF_SESSION_KEY = 'ZDugvrQecxzj6Ko4ChnMQPI9LDTS/pqZ8EIesIh6y14='

# Secret key for signing cookies
SECRET_KEY = '7Ctp2S1Q+TNmwEeVzDjRdEmF4qPGYpXfdOTP0wkBNFk='

MONGODB_SETTINGS = {
    'DB': 'example',
    'USERNAME': 'example',
    'PASSWORD': "example",
    'HOST': 'localhost',
    'PORT': 27017
}

MEDIA = '/media/'
MEDIA_PATH = os.path.join(BASE_DIR, 'media')

STATIC = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, 'static')

APPS = [
    ('/app', 'app'),

]
