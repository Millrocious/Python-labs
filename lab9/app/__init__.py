from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
logger.add("out.log")
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or 'default'))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.contact import contact_bp
        from app.home import home_bp
        from app.auth import auth_bp

        app.register_blueprint(contact_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)

    return app
