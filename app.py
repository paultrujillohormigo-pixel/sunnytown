from flask import Flask, render_template, request, redirect, url_for
import pymysql
from config import DB_CONFIG
import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloudinary_url="cloudinary://667475984668736:FeXuvRmRg_PzdhkyvH2s4Wb9o9M@dnzkctdej"
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
