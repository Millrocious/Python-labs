from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import Email, DataRequired, Length, ValidationError, Regexp, EqualTo

from .models import User


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
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This user already exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email already exists')


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email(message='Invalid Email')])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me: ")
    submit = SubmitField('Sign in')


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=4, max=25,
                                              message='Username length must be between 4 and 25'),
                                       Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                                              message='Username can contains lettes, numbers, dots and underscores')])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(max=120, message='About me is too long')])
    picture = FileField("Profile picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use')


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password',
                             validators=[Length(min=6,
                                                message='Password must be longer then 6')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Reset password")

    def validate_old_password(self, old_password):
        if not current_user.verify_password(old_password.data):
            raise ValidationError('Password is not correct')
