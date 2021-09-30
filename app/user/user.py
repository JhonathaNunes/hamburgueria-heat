from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_required
from app.models import db, User, UserRole, Role
from werkzeug.security import generate_password_hash

user_bp = Blueprint(
    "user", __name__, template_folder="templates", static_folder="static"
)

columns = ["Nome", "Nome do Usuário", "Permissão", "Visualizar"]


@user_bp.route("/admin/user/", methods=["GET"])
@login_required
def index():
    users = User.query.all()

    return render_template(
        "user_listing.j2",
        title="Usuários",
        path_new="/admin/user/new",
        columns=columns,
        data=users
    )


@user_bp.route("/admin/user/new", methods=["GET"])
@login_required
def user_form():
    return render_template(
        "user_form.j2",
        title="Novo usuário",
        action="/admin/user",
        user=None
    )


@user_bp.route("/admin/user", methods=["POST"])
@login_required
def create_user():
    form = request.form

    user = User()

    user.name = form["name"]
    user.username = form["username"]
    user.password = generate_password_hash(form["password"])

    db.session.add(user)
    db.session.flush()

    # Cria role para o usuário
    form_role = form["role"]
    role = Role.query.filter_by(code=form_role).first()
    user_role = UserRole()
    user_role.user_id = user.id
    user_role.role_id = role.id
    db.session.add(user_role)

    db.session.commit()

    flash("Usuário cadastrado com sucesso")
    return redirect(url_for("user.index"))


@user_bp.route("/admin/user/<int:id>", methods=["GET"])
@login_required
def user_view(id: int):
    user = User.query.get(id)
    user_role = UserRole.query.filter_by(user_id=id).first()
    role = Role.query.get(user_role.role_id)

    return render_template(
        "user_form.j2",
        title="Editar usuário",
        user=user,
        role=role,
        action=f"/admin/user/{id}"
    )


@user_bp.route("/admin/user/<int:id>", methods=["DELETE"])
@login_required
def delete_user(id: int):
    # Deleta role do usuário
    user_role = UserRole.query.filter_by(user_id=id).first()
    db.session.delete(user_role)

    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    flash("Usuário deletado com sucesso")
    return {}


@user_bp.route("/admin/user/<int:id>", methods=["POST"])
@login_required
def update_user(id: int):
    form = request.form

    user = User.query.get(id)

    user.name = form["name"]
    user.username = form["username"]
    if form["password"]:
        user.password = form["password"]

    # Atualiza role do usuário
    form_role = form["role"]
    role = Role.query.filter_by(code=form_role).first()
    user_role = UserRole.query.filter_by(user_id=id).first()
    user_role.role_id = role.id

    db.session.commit()

    flash("Usuário atualizado com sucesso")
    return redirect(url_for("user.index"))
