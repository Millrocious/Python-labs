from flask import Blueprint

todo_bp = Blueprint('todo_bp', __name__, template_folder='templates/todo', static_folder='static', static_url_path='/todo-static')

from . import views, models
