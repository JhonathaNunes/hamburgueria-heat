from flask import Blueprint, render_template, request
from app.models import db, Client

client_bp = Blueprint(
    "client", __name__, template_folder="templates", static_folder="static"
)

columns = ["Nome", "Telefone", "CPF", "Visualizar"]


@client_bp.route("/admin/client/<int:id>", methods=["POST"])
def update_client(id: int):
    form = request.form

    client = Client.query.get(id)

    client.full_name = form["full_name"]
    client.phone = form["phone"]
    client.cpf = form["cpf"]
    client.street = form["street"]
    client.number = form["number"]
    client.district = form["district"]

    db.session.commit()

    clients = Client.query.all()

    return render_template(
        "client_listing.j2",
        title="Clientes",
        path_new="/admin/client/new",
        columns=columns,
        data=clients,
        message="Cliente atualizado"
    )


@client_bp.route("/admin/client/", methods=["GET"])
def index():
    clients = Client.query.all()

    return render_template(
        "client_listing.j2",
        title="Clientes",
        path_new="/admin/client/new",
        columns=columns,
        data=clients
    )


@client_bp.route("/admin/client/new", methods=["GET"])
def client_form():
    return render_template(
        "client_form.j2",
        title="Novo cliente",
        action="/admin/client",
        client=None
    )


@client_bp.route("/admin/client", methods=["POST"])
def create_client():
    form = request.form

    client = Client()

    client.full_name = form["full_name"]
    client.phone = form["phone"]
    client.cpf = form["cpf"]
    client.street = form["street"]
    client.number = form["number"]
    client.district = form["district"]

    db.session.add(client)
    db.session.commit()

    clients = Client.query.all()

    return render_template(
        "client_listing.j2",
        title="Clientes",
        path_new="/admin/client/new",
        message="Cliente cadastrado com sucesso",
        columns=columns,
        data=clients
    )


@client_bp.route("/admin/client/<int:id>", methods=["GET"])
def client_view(id: int):
    client = Client.query.get(id)

    return render_template(
        "client_form.j2",
        title="Editar cliente",
        client=client,
        action=f"/admin/client/{id}"
    )


@client_bp.route("/admin/client/<int:id>", methods=["DELETE"])
def delete_client(id: int):
    client = Client.query.get(id)

    db.session.delete(client)
    db.session.commit()

    clients = Client.query.all()

    return render_template(
        "client_listing.j2",
        title="Categorias",
        path_new="/admin/client/new",
        columns=columns,
        data=clients,
        message="Cliente exluído"
    )
