from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
import cloudinary.uploader
from config import DB_CONFIG

# Crear blueprint de productos
products_bp = Blueprint('products', __name__, template_folder='templates')

# Configuración de Cloudinary
cloudinary.config(
    cloud_name="dnzkctdej",
    api_key="667475984668736",
    api_secret="FeXuvRmRg_PzdhkyvH2s4Wb9o9M"
)

# Función para conectar a la DB
def conectar_db():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=int(DB_CONFIG["port"]),
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# Ruta para agregar un producto
@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['name']
        descripcion = request.form['description']
        precio = float(request.form['price'])
        categoria = request.form['category']

        # Subir imagen a Cloudinary
        imagen_file = request.files['image']
        subida = cloudinary.uploader.upload(imagen_file, folder="sunnytown")
        imagen_url = subida["secure_url"]

        # Guardar producto en DB
        db = conectar_db()
        cursor = db.cursor()
        sql = """
        INSERT INTO products (name, description, price, category, main_image)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, descripcion, precio, categoria, imagen_url)
        cursor.execute(sql, valores)
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('products.add_product'))  # redirige a la misma página para agregar más productos

    # Si es GET, solo renderiza el formulario
    return render_template('add_product.html')

# Ruta opcional para listar productos
@products_bp.route('/', methods=['GET'])
def list_products():
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    productos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', products=productos)
