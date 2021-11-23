from os import path, getcwd
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_required
from app.email.mailer import EmailThread
from app.models import db, User, Role
from werkzeug.security import generate_password_hash

from config import Config

user_bp = Blueprint(
    'user', __name__, template_folder='templates', static_folder='static'
)

columns = ['Nome', 'Nome do Usuário', 'Permissão', 'Visualizar']


@user_bp.route('/admin/user/', methods=['GET'])
@login_required
def index():
    users = User.query.all()

    return render_template(
        'user_listing.j2',
        title='Usuários',
        path_new='/admin/user/new',
        columns=columns,
        data=users
    )


@user_bp.route('/admin/user/new', methods=['GET'])
@login_required
def user_form():
    return render_template(
        'user_form.j2',
        title='Novo usuário',
        action='/admin/user',
        user=None
    )


@user_bp.route('/admin/user', methods=['POST'])
@login_required
def create_user():
    form = request.form
    form_role = form['role']
    role = Role.query.filter_by(code=form_role).first()

    user = User()

    user.name = form['name']
    user.username = form['username']
    user.email = form['email']

    user.role = role

    db.session.add(user)
    db.session.commit()

    token = user.get_reset_token()

    entity = {}
    entity['name'] = user.name
    entity['url'] = url_for('login.reset_token', token=token, _external=True)

    params_email = {
        'text_type': 'html',
        'sender': Config.EMAIL_USER,
        'to': form['email'],
        'subject': '🍔🔥 Cadastre sua senha | Hamburgueria Heat! 🔥🍔',
        'template': 'reset_password_mail',
        'entity': entity,
        'images': ['logo.png']
    }

    EmailThread(params_email).start()

    flash('Usuário cadastrado com sucesso')
    return redirect(url_for('user.index'))


@user_bp.route('/admin/user/<int:id>', methods=['GET'])
@login_required
def user_view(id: int):
    user = User.query.get(id)

    return render_template(
        'user_form.j2',
        title='Editar usuário',
        user=user,
        action=f'/admin/user/{id}'
    )


@user_bp.route('/admin/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id: int):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    flash('Usuário deletado com sucesso')
    return {}


@user_bp.route('/admin/user/<int:id>', methods=['POST'])
@login_required
def update_user(id: int):
    form = request.form
    form_role = form['role']
    role = Role.query.filter_by(code=form_role).first()

    user = User.query.get(id)

    user.name = form['name']
    user.username = form['username']
    user.role = role
    if form['password']:
        user.password = form['password']

    db.session.commit()

    flash('Usuário atualizado com sucesso')
    return redirect(url_for('user.index'))
