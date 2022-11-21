from flask import Blueprint, render_template, abort

auth = Blueprint('auth', __name__, template_folder='templates/auth')

from . import views
