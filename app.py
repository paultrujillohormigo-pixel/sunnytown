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
