from flask import Flask, render_template, request, redirect, url_for
import pymysql
from config import DB_CONFIG
import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="TU_CLOUD_NAME",
    api_key="TU_API_KEY",
    api_secret="TU_API_SECRET"
)
app = Flask(__name__)

# Carpeta donde guardamos imágenes
app.config['UPLOAD_FOLDER'] = 'fotoslentes'

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

# Ruta principal para subir productos
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

        # Guardar en DB
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
