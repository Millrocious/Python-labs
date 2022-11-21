from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.candidate_form import candidate_bp
from app.home import home_bp

app = Flask(__name__)
app.config.from_object('config')
logger.add("out.log")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.register_blueprint(home_bp)
app.register_blueprint(candidate_bp)

from app import views, models
