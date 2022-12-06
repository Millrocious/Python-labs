import enum

from app import db


class Priority(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Progress(enum.Enum):
    TODO = "Todo"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class TodoUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Enum(Priority), nullable=False)
    progress = db.Column(db.Enum(Progress), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('todo_user.id'), nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.title
