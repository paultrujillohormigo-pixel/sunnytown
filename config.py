import os
print(os.getenv("RAILWAY_DB_HOST") or os.getenv("MYSQL_HOST"))
print(os.getenv("RAILWAY_DB_PORT") or os.getenv("MYSQL_PORT"))
print(os.getenv("RAILWAY_DB_USER") or os.getenv("MYSQL_USER"))
print(os.getenv("RAILWAY_DB_PASSWORD") or os.getenv("MYSQL_PASSWORD"))
print(os.getenv("RAILWAY_DB_NAME") or os.getenv("MYSQL_DATABASE"))



DB_CONFIG = 
    
    "host": os.getenv("RAILWAY_DB_HOST") or os.getenv("MYSQL_HOST"),
    
    "port": int(os.getenv("RAILWAY_DB_PORT") or os.getenv("MYSQL_PORT")),
    "user": os.getenv("RAILWAY_DB_USER") or os.getenv("MYSQL_USER"),
    "password": os.getenv("RAILWAY_DB_PASSWORD") or os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("RAILWAY_DB_NAME") or os.getenv("MYSQL_DATABASE"),
}
