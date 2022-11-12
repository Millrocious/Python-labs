from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger

app = Flask(__name__)
app.config.from_object('config')
logger.add("out.log")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models
