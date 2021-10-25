from os import path, getcwd
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    send_from_directory
)
from app.models import Category

catalog_bp = Blueprint(
    'catalog', __name__, template_folder='templates'
)


@catalog_bp.route('/', methods=['GET'])
def index():
    categories = Category.query.all()

    for c in categories:
        print(c)
        print(c.products)
    return "Hoi"
