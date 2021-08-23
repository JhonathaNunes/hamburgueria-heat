from flask import Blueprint, render_template

admin_bp = Blueprint(
    "admin", __name__, template_folder="templates", static_folder="static"
)


@admin_bp.route("/admin/", methods=["GET"])
def index():
    return render_template(
        "index.j2",
        title="Hamburgueria Heat"
    )
