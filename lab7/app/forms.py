from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Email, DataRequired, Length, ValidationError, Regexp, EqualTo
from wtforms.widgets import TextArea


class ContactForm(FlaskForm):
    subjects = [('1', 'math'), ('2', 'english'), ('3', 'physics')]
    name = StringField("Name: ",
                       validators=[DataRequired(),
                                   Length(min=4, max=10,
                                          message='Name length must be between %(min)d and %(max)d characters')])
    email = StringField("Email: ", validators=[DataRequired(), Email(message='Invalid Email')])
    phone = StringField('Phone', validators=[DataRequired(message='Wrong Phone'), Length(min=13, max=13),
                                             Regexp(regex='^\+380[0-9]{9}')])
    subject = SelectField("Subject: ", choices=subjects)
    message = StringField("Message: ", widget=TextArea(), validators=[Length(max=500), DataRequired()])
    submit = SubmitField("Send")


class RegistrationForm(FlaskForm):
    username = StringField("Username: ",
                           validators=[DataRequired(),
                                       Length(min=4, max=25,
                                              message='Name length must be between %(min)d and %(max)d characters')])
    email = StringField("Email: ", validators=[DataRequired(), Email(message='Invalid Email')])
    password = PasswordField("Password: ",
                             validators=[Length(min=6, message="Name length must be minimum %(min)d characters long"),
                                         DataRequired()])
    confirm_password = PasswordField('Confirm password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email(message='Invalid Email')])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me: ")
    submit = SubmitField('Sign in')
