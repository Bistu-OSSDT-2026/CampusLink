from flask import Flask

from app.config import Config
from app.blueprints.auth_bp import auth_bp
from app.blueprints.items_bp import items_bp
from app.blueprints.interaction_bp import interaction_bp
from app.blueprints.admin_bp import admin_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(interaction_bp)
    app.register_blueprint(admin_bp)
    
    @app.route('/')
    def index():
        return items_bp.index()
    
    return app