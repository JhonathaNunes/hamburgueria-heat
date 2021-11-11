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

menu_bp = Blueprint(
    'menu', __name__, template_folder='templates'
)


@menu_bp.route('/', methods=['GET'])
def index():
    categories = Category.query.all()

    return render_template('menu_index.j2', categories=categories)
