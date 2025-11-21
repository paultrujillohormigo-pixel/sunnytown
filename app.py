from flask import Flask, render_template, request
from products.routes import products_bp, obtener_productos

app = Flask(__name__)
app.register_blueprint(products_bp)

@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("q", "")
    productos = obtener_productos(search_query)

    return render_template(
        "index.html",
        products=productos,
        search_query=search_query
    )

if __name__ == "__main__":
    app.run(debug=True)
