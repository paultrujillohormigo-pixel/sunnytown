import pymysql
from flask import Flask, render_template, request, redirect, url_for
import cloudinary.uploader
from config import DB_CONFIG
from flask import Flask
from products.routes import products_bp
from sales.routes import sales_bp

app = Flask(__name__)
app.config.from_object('config')

# Registrar blueprints
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(sales_bp, url_prefix='/sales')

if __name__ == '__main__':
    app.run(debug=True)

# Configuración de Cloudinary
cloudinary.config(
    cloud_name="dnzkctdej",
    api_key="667475984668736",
    api_secret="FeXuvRmRg_PzdhkyvH2s4Wb9o9M"
)

app = Flask(__name__)

# Conexión a DB
def conectar_db():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=int(DB_CONFIG["port"]),
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# Función para obtener productos (opcional búsqueda)
def obtener_productos(search=None):
    db = conectar_db()
    cursor = db.cursor()
    if search:
        sql = """
        SELECT id, name, description, price, category, main_image
        FROM products
        WHERE name LIKE %s OR description LIKE %s
        """
        cursor.execute(sql, (f"%{search}%", f"%{search}%"))
    else:
        sql = "SELECT id, name, description, price, category, main_image FROM products"
        cursor.execute(sql)
    productos = cursor.fetchall()
    cursor.close()
    db.close()
    return productos

# Ruta principal con galería dinámica
@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("q")
    productos = obtener_productos(search_query)
    return render_template("index.html", products=productos, search_query=search_query or "")

# Ruta para subir productos
@app.route('/add_product', methods=['GET', 'POST'])
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

        return redirect(url_for('add_product'))

    return render_template('add_product.html')


if __name__ == "__main__":
    app.run(debug=True)
