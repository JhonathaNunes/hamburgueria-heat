from flask import Flask
from config import Config
from .models import db


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        '''
        TODO import blueprints
        TODO register blueprints
        '''
        from .admin import admin
        from .client import client

        app.register_blueprint(admin.admin_bp)
        app.register_blueprint(client.client_bp)

        return app
