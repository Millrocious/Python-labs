from flask import render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user

from . import auth_bp
from .forms import LoginForm, RegistrationForm
from .models import User
from .. import db


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash(f'Please logout to create new account!', category='warning')
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', category='success')
        try:
            db.session.add(User(username=form.username.data,
                                email=form.email.data,
                                password=form.password.data))
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash(f'You already logged in!', category='warning')
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.email == form.email.data and user.verify(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            return redirect(url_for('homepage'))
        else:
            flash('Login unsuccessful. Please check username and password', category='warning')
    return render_template('login.html', form=form, title='Login')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('homepage'))


@auth_bp.route('/users')
def users():
    all_users = User.query.all()
    if all_users:
        return render_template('user_table.html', users=all_users)
    flash('There is no user in the database', category='warning')
    return render_template('user_table.html', users=all_users)


@auth_bp.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

