"""
Production Settings for Heroku
"""
import os
import dotenv
import dj_database_url

#Intializing dotenv to get 7 set environmental variables
dotenv_file = dotenv.find_dotenv(filename='.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

ALLOWED_HOSTS = (os.environ.get('ALLOWED_HOSTS_HEROKU'),)

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=False)
