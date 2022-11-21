from flask import render_template
from . import home


@home.route('/')
@home.route('/home')
def home():
    return render_template('homepage.html', title="Home page")




