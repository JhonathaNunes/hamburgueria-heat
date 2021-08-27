from flask import Blueprint, render_template, request
from app.models import Category, db, Product

product_dp = Blueprint(
    "product", __name__, template_folder="templates", static_folder="static"
)

columns = ["Nome", "Quantidade", "Preço", "Categoria", "Vizualizar"]


@product_dp.route("/admin/product/", methods=["GET"])
def index():
    products = Product.query.all()

    return render_template(
        "product_listing.j2",
        title="Produtos",
        path_new="/admin/product/new",
        columns=columns,
        data=products
    )


@product_dp.route("/admin/product/new", methods=["GET"])
def product_form():
    categories = Category.query.all()

    return render_template(
        "product_form.j2",
        title="Novo produto",
        action="/admin/product",
        categories=categories,
        product=None
    )


@product_dp.route("/admin/product", methods=["POST"])
def create_product():
    form = request.form

    product = Product()

    product.name = form["name"]
    product.description = form["description"]
    product.quantity = int(form["quantity"])
    product.price = float(form["price"])
    product.category_id = int(form["category"])

    db.session.add(product)
    db.session.commit()

    products = Product.query.all()

    return render_template(
        "product_listing.j2",
        title="Produtos",
        path_new="/admin/category/new",
        message="Produto cadastrado",
        columns=columns,
        data=products
    )


@product_dp.route("/admin/product/<int:id>", methods=["GET"])
def product_view(id: int):
    product = Product.query.get(id)
    categories = Category.query.all()

    return render_template(
        "product_form.j2",
        title="Novo produto",
        action=f"/admin/product/{id}",
        categories=categories,
        product=product
    )


@product_dp.route("/admin/product/<int:id>", methods=["DELETE"])
def delete_product(id: int):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    products = Product.query.all()

    return render_template(
        "product_listing.j2",
        title="Produtos",
        path_new="/admin/product/new",
        columns=columns,
        data=products,
        message="Produto exluído"
    )


@product_dp.route("/admin/product/<int:id>", methods=["POST"])
def update_product(id: int):
    form = request.form

    product = Product.query.get(id)

    product.name = form["name"]
    product.description = form["description"]
    product.quantity = int(form["quantity"])
    product.price = float(form["price"])
    product.category_id = int(form["category"])

    db.session.commit()

    products = Product.query.all()

    return render_template(
        "product_listing.j2",
        title="Produtos",
        path_new="/admin/product/new",
        message="Produto autalizado",
        columns=columns,
        data=products
    )
