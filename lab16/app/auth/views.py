import os
import secrets
from functools import wraps

from PIL import Image, ImageOps
from urllib.parse import urlparse, urljoin
from flask import render_template, flash, redirect, url_for, request, abort, current_app, session
from flask_login import login_required, logout_user, login_user, current_user

from . import auth_bp
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ResetPasswordForm
from .models import User
from .. import db


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash(f'Please logout to create new account!', category='warning')
        return redirect(url_for('home.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            db.session.add(User(username=form.username.data,
                                email=form.email.data,
                                password=form.password.data))
            db.session.commit()
            flash(f'Account created for {form.username.data}!', category='success')
        except:
            db.session.rollback()

        return redirect(url_for('home.home'))
    return render_template('register.html', form=form, title='Register')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash(f'You already logged in!', category='warning')
        return redirect(url_for('home.home'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(email=form.email.data).first()
            if user and user.email == form.email.data and user.verify_password(form.password.data):
                login_user(user, remember=form.remember.data)
                session['logged_in'] = True
                flash('You have been logged in!', category='success')
                next = request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)
                return redirect(url_for('home.home'))
            else:
                flash('Login unsuccessful. Please check username and password', category='warning')
                return redirect(url_for('home.home'))
    return render_template('login.html', form=form, title='Login')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash('You have been logged out', category='success')
    return redirect(url_for('home.home'))


@auth_bp.route('/users')
def users():
    all_users = User.query.all()
    if all_users:
        return render_template('user_table.html', users=all_users)
    flash('There is no user in the database', category='warning')
    return render_template('user_table.html', users=all_users)


@auth_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account_profile():
    print(current_user.last_seen)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        flash('Account successfully updated ', category='success')
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_extention = os.path.splitext(form_picture.filename)
    picture_name = random_hex + file_extention
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_name)

    output_size = (125, 125)
    image = Image.open(form_picture)
    thumb = ImageOps.fit(image, output_size, Image.ANTIALIAS)
    thumb.save(picture_path)

    return picture_name


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        flash(f"Password successfully changed", category='success')
        return redirect(url_for('auth.account_profile'))
    return render_template('reset_password.html', form=form)
