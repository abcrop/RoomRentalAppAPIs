"""
Production Settings for Heroku
"""
import dj_database_url

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=False)
