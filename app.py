from flask import Flask, render_template, request
import pymysql
from products.routes import products_bp
from config import DB_CONFIG
import os

def conectar_db():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=int(DB_CONFIG["port"]),
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "secret_key")

    # Registrar Blueprint
    app.register_blueprint(products_bp, url_prefix="/products")

    # --- HOME ---
    @app.route("/")
    def index():
        search = request.args.get("search", "")

        db = conectar_db()
        cursor = db.cursor()

        if search:
            sql = "SELECT * FROM products WHERE name LIKE %s OR description LIKE %s"
            cursor.execute(sql, (f"%{search}%", f"%{search}%"))
        else:
            sql = "SELECT * FROM products"
            cursor.execute(sql)

        productos = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template("index.html", productos=productos, search=search)

    return app


# --- Railway ---
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
