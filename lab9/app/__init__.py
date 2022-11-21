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


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or 'default'))
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from . import views, models

        return app
