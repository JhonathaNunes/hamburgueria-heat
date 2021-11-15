from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_required
from app.models import db, Client

client_bp = Blueprint(
    'client', __name__, template_folder='templates', static_folder='static'
)

columns = ['Nome', 'E-mail', 'Telefone', 'CPF', 'Visualizar']


@client_bp.route('/admin/client/', methods=['GET'])
@login_required
def index():
    clients = Client.query.all()

    return render_template(
        'client_listing.j2',
        title='Clientes',
        path_new='/admin/client/new',
        columns=columns,
        data=clients
    )


@client_bp.route('/admin/client/new', methods=['GET'])
@login_required
def client_form():
    return render_template(
        'client_form.j2',
        title='Novo cliente',
        action='/admin/client',
        client=None
    )


@client_bp.route('/admin/client', methods=['POST'])
@login_required
def create_client():
    form = request.form

    client = Client()

    client.full_name = form['full_name']
    client.phone = form['phone']
    client.cpf = form['cpf']
    client.cep = form['cep']
    client.street = form['street']
    client.number = form['number']
    client.district = form['district']
    client.email = form['email']

    db.session.add(client)
    db.session.commit()

    flash('Cliente cadastrado com sucesso')
    return redirect(url_for('client.index'))


@client_bp.route('/admin/client/<int:id>', methods=['GET'])
@login_required
def client_view(id: int):
    client = Client.query.get(id)

    return render_template(
        'client_form.j2',
        title='Editar cliente',
        client=client,
        action=f'/admin/client/{id}'
    )


@client_bp.route('/admin/client/<int:id>', methods=['DELETE'])
@login_required
def delete_client(id: int):
    client = Client.query.get(id)

    db.session.delete(client)
    db.session.commit()

    flash('Cliente deletado com sucesso')
    return {}


@client_bp.route('/admin/client/<int:id>', methods=['POST'])
@login_required
def update_client(id: int):
    form = request.form

    client = Client.query.get(id)

    client.full_name = form['full_name']
    client.phone = form['phone']
    client.cpf = form['cpf']
    client.cep = form['cep']
    client.street = form['street']
    client.number = form['number']
    client.district = form['district']
    client.email = form['email']

    db.session.commit()

    flash('Cliente atualizado com sucesso')
    return redirect(url_for('client.index'))
