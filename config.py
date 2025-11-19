import os


DB_CONFIG = {
    
    "host": os.getenv("DB_HOST") or os.getenv("MYSQL_HOST"),
    "port": (os.getenv("DB_PORT") or os.getenv("MYSQL_PORT")),
    "user": os.getenv("DB_USER") or os.getenv("MYSQL_USER"),
    "password": os.getenv("DB_PASSWORD") or os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("DB_NAME") or os.getenv("MYSQL_DATABASE"),
}
