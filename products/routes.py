from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
import cloudinary
import cloudinary.uploader
from config import DB_CONFIG
import mercadopago
import os


cloudinary.config(
    cloud_name="dnzkctdej",
    api_key="667475984668736",
    api_secret="FeXuvRmRg_PzdhkyvH2s4Wb9o9M"
)


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
        sql = "INSERT INTO products (code, name, description, price, category, main_image) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (codigo, nombre, descripcion, precio, categoria, imagen_url))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("products.add_product"))

    return render_template("add_product.html")


# --- Ruta para ver un producto individual ---
@products_bp.route("/<int:product_id>")
def ver_producto(product_id):
    db = conectar_db()
    cursor = db.cursor()
    sql = "SELECT * FROM products WHERE id = %s"
    cursor.execute(sql, (product_id,))
    producto = cursor.fetchone()
    cursor.close()
    db.close()

    if not producto:
        return "Producto no encontrado", 404

    return render_template("product_detail.html", producto=producto)


# --- Crear cobro Mercado Pago ---
@products_bp.route("/crear_pago", methods=["POST"])
def crear_pago():
    data = request.get_json()

    product_id = data.get("product_id")
    amount = float(data.get("amount"))
    title = data.get("title", "Producto")

    sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

    preference_data = {
        "items": [{
            "title": title,
            "quantity": 1,
            "unit_price": amount,
            "currency_id": "MXN"
        }],
        "back_urls": {
            "success": url_for("products.ver_producto", product_id=product_id, _external=True),
            "failure": url_for("products.ver_producto", product_id=product_id, _external=True)
        },
        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)
    link = preference["response"]["init_point"]

    return {"link": link}

