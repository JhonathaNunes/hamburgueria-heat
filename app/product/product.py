from os import path, getcwd, remove
from uuid import uuid1
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    send_from_directory
)
from flask_login.utils import login_required
from app.models import Category, db, Product
from werkzeug import exceptions

product_dp = Blueprint(
    'product', __name__, template_folder='templates', static_folder='static'
)

columns = ['Nome', 'Quantidade', 'Preço', 'Categoria', 'Vizualizar']


def get_extension(filename: str) -> str:
    if '.' not in filename:
        return ''

    return filename.rsplit('.', 1)[1].lower()


def save_file_upload() -> str:
    if "file" not in request.files:
        return None

    file = request.files["file"]
    ext = get_extension(file.filename)

    if ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
        u = uuid1()
        filename = f"{u}.{ext}"
        file.save(path.join('product_pic', filename))

        return filename


def delete_file(file_id):
    if not file_id:
        return

    file_path = path.join('product_pic', file_id)
    if path.exists(file_path):
        remove(file_path)


@product_dp.route('/admin/product/file/<file_id>')
def download_file(file_id):
    project_path = path.abspath(getcwd())

    try:
        return send_from_directory(f'{project_path}/product_pic', file_id)
    except exceptions.NotFound:
        return send_from_directory('static/images', 'no-photo.png')


@product_dp.route('/admin/product/', methods=['GET'])
@login_required
def index():
    products = Product.query.all()

    return render_template(
        'product_listing.j2',
        title='Produtos',
        path_new='/admin/product/new',
        columns=columns,
        data=products
    )


@product_dp.route('/admin/product/new', methods=['GET'])
@login_required
def product_form():
    categories = Category.query.all()

    return render_template(
        'product_form.j2',
        title='Novo produto',
        action='/admin/product',
        categories=categories,
        product=None
    )


@product_dp.route('/admin/product', methods=['POST'])
@login_required
def create_product():
    form = request.form

    product = Product()

    product.name = form['name']
    product.description = form['description']
    product.quantity = int(form['quantity']) if (form['quantity']) else None
    product.price = float(form['price'])
    product.category_id = int(form['category'])
    product.photo_url = save_file_upload()

    db.session.add(product)
    db.session.commit()

    flash('Produto cadastrado com sucesso')
    return redirect(url_for('product.index'))


@product_dp.route('/admin/product/<int:id>', methods=['GET'])
@login_required
def product_view(id: int):
    product = Product.query.get(id)
    categories = Category.query.all()

    return render_template(
        'product_form.j2',
        title='Editar produto',
        action=f'/admin/product/{id}',
        categories=categories,
        product=product
    )


@product_dp.route('/admin/product/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id: int):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    delete_file(product.photo_url)

    flash('Produto deletado com sucesso')
    return {}


@product_dp.route('/admin/product/<int:id>', methods=['POST'])
@login_required
def update_product(id: int):
    form = request.form

    product = Product.query.get(id)

    old_product_photo = product.photo_url

    product.name = form['name']
    product.description = form['description']
    product.quantity = int(form['quantity']) if (form['quantity']) else None
    product.price = float(form['price'])
    product.category_id = int(form['category'])
    product.photo_url = save_file_upload()

    db.session.commit()

    if "file" in request.files and old_product_photo:
        delete_file(old_product_photo)

    flash('Produto atualizado com sucesso')
    return redirect(url_for('product.index'))
