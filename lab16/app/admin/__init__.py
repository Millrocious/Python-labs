from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.admin.models import UserModelView
from app.auth.models import User
from app.todo.models import Task, Category

admin = Admin(name='Flask Site', template_mode='bootstrap3')


def create_module(app, db, **kwargs):
    admin.init_app(app)

    admin.add_view(UserModelView(User, db.session, name='Users'))
    admin.add_view(ModelView(Task, db.session, name='Tasks'))
    admin.add_view(ModelView(Category, db.session, name='Categories'))
