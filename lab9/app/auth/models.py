from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    # image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    password = db.Column(db.String(40), unique=False, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return '<User %r>' % self.username
