from flask import Blueprint, render_template, request
from app.models import db, Category

category_bp = Blueprint(
    "category", __name__, template_folder="templates", static_folder="static"
)


@category_bp.route("/admin/category/", methods=["GET"])
def index():
    categories = Category.query.all()

    print(categories)
    return render_template(
        "category_listing.j2",
        title="Categorias",
        path_new="/admin/category/new",
        columns=["Nome", "Descrição", "Visualizar"],
        data=categories
    )


@category_bp.route("/admin/category/new", methods=["GET"])
def category_form():
    return render_template(
        "category_form.j2",
        title="Nova categoria"
    )


@category_bp.route("/admin/category", methods=["POST"])
def create_category():
    form = request.form

    category = Category()

    category.name = form["name"]
    category.description = form["description"]

    db.session.add(category)
    db.session.commit()

    return render_template(
        "category_listing.j2",
        title="Categorias",
        path_new="/admin/category/new",
        message="Categoria cadastrada com sucesso"
    )
