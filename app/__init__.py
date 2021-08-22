from flask import Flask
from config import Config


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    with app.app_context():
        '''
        TODO import blueprints
        TODO register blueprints
        '''
        from .admin import admin

        app.register_blueprint(admin.admin_bp)

        return app
