from click import echo
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config
import sqlalchemy as sa

db = SQLAlchemy()
logger.add("out.log")
migrate = Migrate()
bcrypt = Bcrypt()
SECRET_KEY = None
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

    global SECRET_KEY
    SECRET_KEY = app.secret_key

    register_cli_commands(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        app.logger.info('Initialized the database!')

        from app.contact import contact_bp
        from app.home import home_bp
        from app.auth import auth_bp
        from app.todo import todo_bp
        from app.category_api import category_bp
        from app.task_api import task_api_bp
        from app.swagger import swagger_bp

        app.register_blueprint(contact_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(category_bp, url_prefix='/api')
        app.register_blueprint(task_api_bp, url_prefix='/api/v2')
        app.register_blueprint(swagger_bp)

    return app


def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')



