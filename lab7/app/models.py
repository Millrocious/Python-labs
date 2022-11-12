from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    phone = db.Column(db.String(40), unique=True, nullable=False)
    subject = db.Column(db.String(40), unique=False, nullable=False)
    message = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.name


class User(db.Model):
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
