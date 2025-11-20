
from flask import Blueprint, render_template, request

sales_bp = Blueprint('sales', __name__, template_folder='templates')

sales_bp = Blueprint('sales', __name__, template_folder='templates')

@sales_bp.route('/sales')
def list_sales():
    return render_template('list_sales.html')

@sales_bp.route('/sales/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        # lógica para agregar venta
        pass
    return render_template('add_sale.html')
