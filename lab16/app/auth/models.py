from sqlalchemy.sql.functions import now
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. import db, login_manager, bcrypt


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    about_me = db.Column(db.String(120), nullable=True)
    last_seen = db.Column(db.DateTime, default=now())
    admin = db.Column(db.Boolean, default=False, unique=False)
    password_hashed = db.Column(db.String(40), unique=False, nullable=False)
    tasks_owned = db.relationship('Task', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Is not readable')

    @password.setter
    def password(self, password):
        self.password_hashed = bcrypt.generate_password_hash(password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hashed, password)

    def __repr__(self):
        return '<User %r>' % self.username
