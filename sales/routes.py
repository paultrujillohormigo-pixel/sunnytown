from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
from config import DB_CONFIG

sales_bp = Blueprint('sales', __name__, template_folder='templates')

# Función para conectar a la DB (puedes importarla desde utils si quieres)
def conectar_db():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=int(DB_CONFIG["port"]),
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

@sales_bp.route('/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        producto = request.form['product']
        cantidad = int(request.form['quantity'])
        precio = float(request.form['price'])

        # Guardar en DB
        db = conectar_db()
        cursor = db.cursor()
        sql = """
        INSERT INTO sales (product, quantity, price)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (producto, cantidad, precio))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('sales.list_sales'))  # redirige a la lista de ventas

    return render_template('add_sale.html')

@sales_bp.route('/', methods=['GET'])
def list_sales():
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sales")
    ventas = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('list_sales.html', sales=ventas)
