from flask import (
    Blueprint,
    render_template,
    request,
    json
)
from app.models import Order, OrderProduct, db, Category, Client, PixModel, Product
from rstr import xeger

menu_bp = Blueprint(
    'menu', __name__, template_folder='templates'
)


@menu_bp.route('/', methods=['GET'])
def index():
    categories = Category.query.all()

    return render_template('menu_index.j2', categories=categories)


def joinProductAndQuantity(product: Product, items: list) -> dict:
    quantity = list(filter(
        lambda el: el['id'] == product.id, items)
    )[0]['quantity']

    product_dict = product.__dict__
    del product_dict['quantity']
    product_dict['qt_ordered'] = quantity
    product_dict['price_formatted'] = "R$ {:,.2f}".format(
        product_dict['price']
    )

    return product_dict


@menu_bp.route('/client/self-register', methods=['GET'])
def self_register_view():
    return render_template('client-self-register.j2')


@menu_bp.route('/client/self-register', methods=['POST'])
def client_self_register():
    form = request.get_json()

    is_new_client = False
    client = Client.query.filter_by(cpf=form['cpf']).first()

    if client is None:
        client = Client()
        is_new_client = True

    client.full_name = form['full_name']
    client.phone = form['phone']
    client.cep = form['cep']
    client.cpf = form['cpf']
    client.street = form['street']
    client.number = form['number']
    client.district = form['district']
    client.email = form['email']

    if is_new_client:
        db.session.add(client)

    db.session.commit()

    return do_checkout(client, json.loads(form.get('bag')))


def do_checkout(client: Client, bag: list):
    with db.session.no_autoflush:
        order = Order()
        order.client = client
        products_id = list(map(lambda el: el['id'], bag))
        products = Product.query.filter(Product.id.in_(products_id)).all()
        order_products = []

        for item in bag:
            order_product = OrderProduct()
            order_product.product = list(filter(
                lambda product: product.id == item['id'],
                products
            ))[0]
            order_product.quantity = item['quantity']
            order_products.append(order_product)

        db.session.add_all(order_products)

        order.products.extend(order_products)

        txid = xeger(r'^[a-zA-Z0-9]{26,35}$')
        order.txid = txid
        order.status_id = 1
        print(order.status_id)

        # O valor está fixo no payload porque está usando api de produçao
        payload = {
            "calendario": {
                "expiracao": 3600
            },
            "valor": {
                "original": "1.00"
            },
            "chave": "e76ed44e-cc9c-47d8-b092-61da1a5443a9"
        }

        pix = PixModel()

        qr_code = pix.create_charge(txid, payload)
        db.session.add(order)
        db.session.commit()

        return render_template('qr_code.j2', qr_code=qr_code)


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

    return render_template(
        'checkout.j2',
        products=products_with_qtd,
        total="R$ {:,.2f}".format(total)
    )



