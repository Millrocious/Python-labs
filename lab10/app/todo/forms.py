from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import Email, DataRequired, Length, ValidationError, Regexp, EqualTo
from wtforms.widgets import TextArea


class TaskForm(FlaskForm):
    priorities = [('1', 'Low'), ('2', 'Medium'), ('3', 'High')]
    title = StringField("Title: ",
                        validators=[DataRequired(),
                                    Length(min=4, max=10,
                                           message='Name length must be between %(min)d and %(max)d characters')])
    description = StringField("Message: ", widget=TextArea(), validators=[Length(max=500), DataRequired()])
    deadline = DateField("Deadline: ", format="%d/%m/%Y", validators=[DataRequired()])
    priority = SelectField("Priority: ", choices=priorities)
    submit = SubmitField("Send")
