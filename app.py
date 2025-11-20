from flask import Flask, render_template, request
from products.routes import products_bp, obtener_productos
from sales.routes import sales_bp

app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(sales_bp, url_prefix="/sales")

# Ruta principal: index
@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("q") or ""
    productos = obtener_productos(search_query)
    return render_template("index.html", products=productos, search_query=search_query)

if __name__ == "__main__":
    app.run(debug=True)
