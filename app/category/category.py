from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_required
from app.models import db, Category

category_bp = Blueprint(
    'category', __name__, template_folder='templates', static_folder='static'
)

columns = ['Nome', 'Descrição', 'Visualizar']


@category_bp.route('/admin/category/', methods=['GET'])
@login_required
def index():
    categories = Category.query.all()

    return render_template(
        'category_listing.j2',
        title='Categorias',
        path_new='/admin/category/new',
        columns=columns,
        data=categories
    )


@category_bp.route('/admin/category/new', methods=['GET'])
@login_required
def category_form():
    return render_template(
        'category_form.j2',
        title='Nova categoria',
        action='/admin/category',
        category=None
    )


@category_bp.route('/admin/category', methods=['POST'])
@login_required
def create_category():
    form = request.form

    category = Category()

    category.name = form['name']
    category.description = form['description']

    db.session.add(category)
    db.session.commit()

    flash('Categoria cadastrado com sucesso')
    return redirect(url_for('category.index'))


@category_bp.route('/admin/category/<int:id>', methods=['GET'])
@login_required
def category_view(id: int):
    category = Category.query.get(id)

    return render_template(
        'category_form.j2',
        title='Editar categoria',
        category=category,
        action=f'/admin/category/{id}'
    )


@category_bp.route('/admin/category/<int:id>', methods=['DELETE'])
@login_required
def delete_category(id: int):
    category = Category.query.get(id)

    db.session.delete(category)
    db.session.commit()

    flash('Categoria excluída com sucesso')
    return {}


@category_bp.route('/admin/category/<int:id>', methods=['POST'])
@login_required
def update_category(id: int):
    form = request.form

    category = Category.query.get(id)

    category.name = form['name']
    category.description = form['description']
    db.session.commit()

    flash('Categoria atualizada com sucesso')
    return redirect(url_for('category.index'))
