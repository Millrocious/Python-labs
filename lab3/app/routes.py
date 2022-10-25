from flask import render_template, request
import platform
import datetime

from app import app

os_info = platform.platform()
url = "http://127.0.0.1:5000/home"


@app.route('/')
@app.route('/home')
def homepage():
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    return render_template('homepage.html', title='Home', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/for_example')
def for_example():
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    return render_template('for_example.html', title='For example', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/if_example')
def if_example():
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    return render_template('if_example.html', title='If example', os_info=os_info, user_agent=user_agent, current_time=current_time)
