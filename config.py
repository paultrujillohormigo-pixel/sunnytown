import os

DB_CONFIG = {
    "host": os.getenv("RAILWAY_DB_HOST"),
    "port": int(os.getenv("RAILWAY_DB_PORT")),
    "user": os.getenv("RAILWAY_DB_USER"),
    "password": os.getenv("RAILWAY_DB_PASS"),
    "database": os.getenv("RAILWAY_DB_NAME"),
}
