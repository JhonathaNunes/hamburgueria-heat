from flask import Blueprint, render_template, request, flash
from werkzeug.utils import redirect
from app.models import db, Category

category_bp = Blueprint(
    "category", __name__, template_folder="templates", static_folder="static"
)

columns = ["Nome", "Descrição", "Visualizar"]


@category_bp.route("/admin/category/", methods=["GET"])
def index():
    categories = Category.query.all()

    return render_template(
        "category_listing.j2",
        title="Categorias",
        path_new="/admin/category/new",
        columns=columns,
        data=categories
    )


@category_bp.route("/admin/category/new", methods=["GET"])
def category_form():
    return render_template(
        "category_form.j2",
        title="Nova categoria",
        action="/admin/category",
        category=None
    )


@category_bp.route("/admin/category", methods=["POST"])
def create_category():
    form = request.form

    category = Category()

    category.name = form["name"]
    category.description = form["description"]

    db.session.add(category)
    db.session.commit()

    flash("Cliente cadastrado com sucesso")
    return redirect("/admin/category/")


@category_bp.route("/admin/category/<int:id>", methods=["GET"])
def category_view(id: int):
    category = Category.query.get(id)

    return render_template(
        "category_form.j2",
        title="Editar categoria",
        category=category,
        action=f"/admin/category/{id}"
    )


@category_bp.route("/admin/category/<int:id>", methods=["DELETE"])
def delete_category(id: int):
    category = Category.query.get(id)

    db.session.delete(category)
    db.session.commit()

    flash("Cliente cadastrado com sucesso")
    return redirect("/admin/category/")


@category_bp.route("/admin/category/<int:id>", methods=["POST"])
def update_category(id: int):
    form = request.form

    category = Category.query.get(id)

    category.name = form["name"]
    category.description = form["description"]
    db.session.commit()

    flash("Cliente cadastrado com sucesso")
    return redirect("/admin/category/")
