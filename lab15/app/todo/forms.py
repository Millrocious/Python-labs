
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email
from flask_ckeditor import CKEditorField

from app.todo.models import Category, Priority, Progress


def get_category_list():
    return [(cat.id, cat.name) for cat in Category.query.all()]


class TaskForm(FlaskForm):
    title = StringField("Title",
                        [DataRequired("Please enter task title."),
                         Length(min=4, max=100, message='Це поле має бути довжиною між 4 та 10 символів')
                         ])
    description = CKEditorField('Description',
                                validators=[Length(max=2048, message='Це поле має бути довжиною до 2048 символів')])
    deadline = DateField('Deadline')
    priority = SelectField(
        'Priority',
        choices=[(name, name) for name in Priority._member_names_],
        render_kw={"class": "form-select"}
    )
    progress = SelectField(
        'Priority',
        choices=[(name, name) for name in Progress._member_names_],
        render_kw={"class": "form-select"}
    )
    category = SelectField("Category")
    submit = SubmitField("Send")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = get_category_list()


class CategoryForm(FlaskForm):
    name = StringField("Name",
                       [DataRequired("Please enter category name."),
                        Length(min=4, max=100, message='Це поле має бути довжиною між 4 та 10 символів')])
    submit = SubmitField("Send")


class AssignUserForm(FlaskForm):
    email = StringField("Email",
                       [DataRequired(),
                        Length(min=4, max=100, message='Це поле має бути довжиною між 4 та 100 символів'),
                        Email()])
    submit = SubmitField("Send")


class CommentForm(FlaskForm):
    text = CKEditorField("Type your comment below",
                         [Length(min=20, max=1000, message='Це поле має бути довжиною між 20 та 1000 символів')])
    submit = SubmitField("Send")
