from datetime import datetime, timedelta
import enum

from app import db


class Priority(enum.Enum):
    low = 1
    medium = 2
    high = 3


class Progress(enum.Enum):
    todo = 1
    doing = 2
    done = 3


def tomorrow_date():
    return datetime.now() + timedelta(days=1)


task_user = db.Table('task_user',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
                     )


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(2048), nullable=True, default=None)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    deadline = db.Column(db.DateTime, default=tomorrow_date)
    priority = db.Column(db.Enum(Priority), default='low')
    progress = db.Column(db.Enum(Progress), default='todo')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User', secondary=task_user, backref=db.backref('tasks', lazy='dynamic'), lazy='dynamic')
    comments = db.relationship('Comment', backref='tasks', lazy='dynamic')

    def __repr__(self):
        return f"Task('{self.title}', '{self.progress}')"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='categories', lazy='dynamic')

    def __repr__(self):
        return f"Category('{self.name}')"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(2048))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
