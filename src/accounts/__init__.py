# src/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config as env_config
import importlib

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Lấy config class từ .env
    config_path = env_config("APP_SETTINGS", default="config.DevelopmentConfig")
    module_name, class_name = config_path.rsplit(".", 1)
    config_class = getattr(importlib.import_module(module_name), class_name)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import các models và đăng ký blueprint
    from src.accounts import views, models
    from src.core import views as core_views

    app.register_blueprint(views.accounts_bp)
    app.register_blueprint(core_views.core_bp)

    return app
