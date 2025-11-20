from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import pymysql
import cloudinary
import cloudinary.uploader
from config import DB_CONFIG
import mercadopago

products_bp = Blueprint("products", __name__, template_folder="templates")

# ==========================
# CONFIG CLOUDINARY
# ==========================
cloudinary.config(
    cloud_name="dxud6raij",
    api_key="371919726857367",
    api_secret="MlGFONo_GAFRUHZdlUVvU1gFzRA",
    secure=True
)

# ==========================
# CONEXIÓN A BD
# ==========================
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )


# ==========================
# LISTADO DE PRODUCTOS
# ==========================
@products_bp.route("/")
def list_products():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
        products = cursor.fetchall()
    conn.close()

    return render_template("products/list.html", products=products)


# ==========================
# CREAR PREFERENCIA MERCADO PAGO
# ==========================
@products_bp.route("/crear_pago", methods=["POST"])
def crear_pago():
    data = request.get_json()

    product_id = data.get("product_id")
    amount = float(data.get("amount"))
    title = data.get("title", "Producto")

    # SDK MERCADO PAGO
    sdk = mercadopago.SDK("APP_USR-4062760235903-112018-12059659646503501b5039e406779672-216274319")

    preference_data = {
        "items": [{
            "title": title,
            "quantity": 1,
            "unit_price": amount,
            "currency_id": "MXN"
        }],
        "back_urls": {
            "success": "https://sunnytown-production.up.railway.app/products/pago_exitoso",
            "failure": "https://sunnytown-production.up.railway.app/products/pago_fallido",
            "pending": "https://sunnytown-production.up.railway.app/products/pago_pendiente"
        },
        "notification_url": "https://sunnytown-production.up.railway.app/products/notificacion_mp",
        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)
    print("DEBUG MP RESPONSE:", preference)

    if "response" not in preference or "init_point" not in preference["response"]:
        return {"error": "No se pudo generar el link de pago"}, 400

    return {"link": preference["response"]["init_point"]}


# ==========================
# CALLBACKS MERCADO PAGO
# ==========================
@products_bp.route("/pago_exitoso")
def pago_exitoso():
    return "Pago exitoso 😎"

@products_bp.route("/pago_fallido")
def pago_fallido():
    return "El pago falló ❌"

@products_bp.route("/pago_pendiente")
def pago_pendiente():
    return "Pago pendiente ⏳"

@products_bp.route("/notificacion_mp", methods=["POST"])
def notificacion_mp():
    # Mercado Pago manda notificaciones aquí (no necesitas procesarlas ahora)
    return "OK", 200


# ==========================
# SUBIR PRODUCTO (OPCIONAL)
# ==========================
@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        category = request.form["category"]

        image = request.files["image"]
        result = cloudinary.uploader.upload(image)
        image_url = result["secure_url"]

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO products (name, description, price, category, main_image)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, description, price, category, image_url))
            conn.commit()
        conn.close()

        return redirect(url_for("products.list_products"))

    return render_template("products/add.html")
