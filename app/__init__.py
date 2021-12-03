from flask import Flask
from flask_login.login_manager import LoginManager
from config import Config
from .models import db, User


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        db.create_all()

        from .login import login
        from .admin import admin
        from .client import client
        from .category import category
        from .user import user
        from .product import product
        from .orders import orders
        from .menu import menu

        app.register_blueprint(login.login_bp)
        app.register_blueprint(admin.admin_bp)
        app.register_blueprint(client.client_bp)
        app.register_blueprint(category.category_bp)
        app.register_blueprint(user.user_bp)
        app.register_blueprint(product.product_dp)
        app.register_blueprint(orders.orders_bp)
        app.register_blueprint(menu.menu_bp)

        login_manager = LoginManager()
        login_manager.login_message = '''É preciso estar logado para acessar
             essa página!'''
        login_manager.login_view = 'login.render_login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        return app
