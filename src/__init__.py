from config import DevelopmentConfig as config_class
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from decouple import config
import os

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # 🔧 Trỏ Flask đến src/templates
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    app = Flask(__name__, template_folder=template_dir)

    # Cấu hình
    app.config.from_object(config_class)

    # Khởi tạo các extension
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import các Blueprint

    from src.accounts.views import accounts_bp
    from src.core.views import core_bp
    from src.lessons.views import lessons_bp
    from src.practice.views import practice_bp
    from src.ai.views import ai_bp
    from src.admin.views import admin_bp
    from src.accounts.models import User

    # Đăng ký blueprint
    app.register_blueprint(core_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)

    # Cấu hình đăng nhập
    login_manager.login_view = "accounts.login"
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
