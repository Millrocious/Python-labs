from flask import Blueprint

home = Blueprint('home', __name__, template_folder='templates/home')

from . import views
