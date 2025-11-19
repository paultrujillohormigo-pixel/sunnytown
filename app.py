from flask import Flask, render_template, request, redirect, url_for
import pymysql
from config import DB_CONFIG
import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
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

# Ruta para subir productos
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['name']
        descripcion = request.form['description']
        precio = float(request.form['price'])
        categoria = request.form['category']

        # SUBIR A CLOUDINARY
        imagen_file = request.files['image']
        subida = cloudinary.uploader.upload(imagen_file, folder="sunnytown")

        # URL pública de la imagen
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
