from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
import cloudinary.uploader
from config import DB_CONFIG

products_bp = Blueprint("products", __name__, template_folder="templates")

# --- Función para DB ---
def conectar_db():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=int(DB_CONFIG["port"]),
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Función que se puede importar desde app.py ---
def obtener_productos(search=None):
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
    return productos

# --- Ruta para agregar productos ---
@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        codigo = request.form["code"]
        nombre = request.form["name"]
        descripcion = request.form["description"]
        precio = float(request.form["price"])
        categoria = request.form["category"]
        

        # Subir imagen a Cloudinary
        imagen_file = request.files["image"]
        subida = cloudinary.uploader.upload(imagen_file, folder="sunnytown")
        imagen_url = subida["secure_url"]

        # Guardar en DB
        db = conectar_db()
        cursor = db.cursor()
        sql = "INSERT INTO products (code,name, description, price, category, main_image) VALUES (%s, %s, %s, %s, %s,%s)"
        cursor.execute(sql, (codigo,nombre, descripcion, precio, categoria, imagen_url))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("products.add_product"))

    return render_template("add_product.html")
