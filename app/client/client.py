from flask import Blueprint, render_template

client_bp = Blueprint(
    "client", __name__, template_folder="templates", static_folder="static"
)


@client_bp.route("/admin/client/", methods=["GET"])
def index():
    return render_template(
        "listing_base.j2",
        title="Clientes"
    )
