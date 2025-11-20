# db.py
import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )
    return conn

def get_products(search=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if search:
        cursor.execute("""
            SELECT id, name, description, price, category, main_image
            FROM products
            WHERE name LIKE %s OR description LIKE %s
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT id, name, description, price, category, main_image FROM products")
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products
