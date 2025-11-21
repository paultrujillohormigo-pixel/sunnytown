@@ -131,3 +131,20 @@ def add_product():
        return redirect(url_for("products.list_products"))

    return render_template("products/add.html")

# --- Función que se puede importar desde app.py ---
def obtener_productos(search=None):
    from .routes import conectar_db   # o usa la función que ya tienes
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
