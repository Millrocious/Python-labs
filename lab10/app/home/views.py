from flask import render_template
from . import home_bp


@home_bp.route('/')
@home_bp.route('/home')
def home():
    return render_template('homepage.html', title="Home page")




