"""
Production Settings for Heroku
"""
import dj_database_url
import dotenv
import os

dotenv_file = dotenv.find_dotenv(filename='.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

ALLOWED_HOSTS = ['roomrentalapis.herokuapp.com', 'roomrentalapis.com', ]

dotenv.set_key(dotenv_file, 'DEBUG', 'False')
DEBUG = os.environ.get('DEBUG')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=False)
