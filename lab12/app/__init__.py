from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
logger.add("out.log")
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or 'default'))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.contact import contact_bp
        from app.home import home_bp
        from app.auth import auth_bp
        from app.todo import todo_bp
        from app.category_api import category_bp

        app.register_blueprint(contact_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(category_bp, url_prefix='/api')

    return app
