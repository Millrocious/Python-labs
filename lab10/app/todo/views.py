from flask import render_template
from . import todo_bp


@todo_bp.route('/task')
def task():
    return render_template('task.html', title="Tasks")




