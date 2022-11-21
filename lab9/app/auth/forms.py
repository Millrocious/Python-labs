from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length, ValidationError, Regexp, EqualTo

from .. import db
from app.auth.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username: ",
                           validators=[DataRequired(),
                                       Length(min=4, max=25,
                                              message='Name length must be between %(min)d and %(max)d characters'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'username must have only letters'
                                                                             ', numbers, dots or underscores')])
    email = StringField("Email: ", validators=[DataRequired(), Email(message='Invalid Email')])
    password = PasswordField("Password: ",
                             validators=[Length(min=6, message="Name length must be minimum %(min)d characters long"),
                                         DataRequired()])
    confirm_password = PasswordField('Confirm password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).first():
            raise ValidationError('This user already exists')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('This email already exists')


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email(message='Invalid Email')])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me: ")
    submit = SubmitField('Sign in')
