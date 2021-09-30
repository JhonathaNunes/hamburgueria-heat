from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_user
from werkzeug.security import check_password_hash
from app.models import User

login_bp = Blueprint(
    "login", __name__, template_folder="templates"
)


@login_bp.route("/login/", methods=["GET"])
def render_login():
    return render_template("login.j2")


@login_bp.route("/login/", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Não foi possível fazer login. Usuário ou senha incorretos')
        return redirect(url_for('login.render_login'))

    login_user(user)
    return redirect(url_for('admin.index'))
