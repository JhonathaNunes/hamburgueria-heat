from flask import Blueprint, render_template
from app.models import Order

orders_bp = Blueprint(
    'order', __name__, template_folder='templates'
)


@orders_bp.route('/admin/order')
def index():
    orders = Order.query.all()

    return render_template(
        'order_listing.j2',
        title='Pedidos',
        data=orders
    )
