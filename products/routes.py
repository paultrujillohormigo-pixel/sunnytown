from flask import Blueprint, render_template, request

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def index():
    return render_template('index.html')

@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # lógica para agregar producto
        pass
    return render_template('add_product.html')
