from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.candidate_form import candidate_bp
from app.home import home_bp
from config import config

db = SQLAlchemy()
logger.add("out.log")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or 'default'))
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(home_bp)
    app.register_blueprint(candidate_bp)

    with app.app_context():
        from app import views, models
