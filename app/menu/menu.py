from os import path, getcwd
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    send_from_directory,
    jsonify
)
from app.models import Category, PixModel, Product
from rstr import xeger

menu_bp = Blueprint(
    'menu', __name__, template_folder='templates'
)


@menu_bp.route('/', methods=['GET'])
def index():
    categories = Category.query.all()

    return render_template('menu_index.j2', categories=categories)


def joinProductAndQuantity(product: Product, items: list) -> dict:
    quantity = list(filter(lambda el: el['id'] == product.id, items))[0]['quantity']

    product_dict = product.__dict__
    del product_dict['quantity']
    product_dict['qt_ordered'] = quantity

    return product_dict


@menu_bp.route('/checkout', methods=['POST'])
def checkout():
    items = request.get_json()
    products_id = list(map(lambda el: el['id'], items))
    products = Product.query.filter(Product.id.in_(products_id)).all()
    products_with_qtd = []
    total = 0

    for product in products:
        product_qtd = joinProductAndQuantity(product, items)
        products_with_qtd.append(product_qtd)
        total += product.price * product_qtd['qt_ordered']

    return render_template('checkout.j2', products=products_with_qtd, total=total)


@menu_bp.route('/docheckout', methods=['POST'])
def do_checkout():
    txid = xeger(r'^[a-zA-Z0-9]{26,35}$')
    payload = {
        "calendario": {
            "expiracao": 3600
        },
        "valor": {
            "original": "5.00"
        },
        "chave": "e76ed44e-cc9c-47d8-b092-61da1a5443a9"
    }

    pix = PixModel()

    response = pix.create_charge(txid, payload)
    return response
