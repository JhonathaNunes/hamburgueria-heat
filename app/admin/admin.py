from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint(
    'admin', __name__, template_folder='templates', static_folder='static'
)


@admin_bp.route('/admin/', methods=['GET'])
@login_required
def index():
    return render_template(
        'index.j2',
        title='Hamburgueria Heat'
    )
