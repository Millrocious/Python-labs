from flask_login import UserMixin

from app import db


class Contact(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    phone = db.Column(db.String(40), unique=True, nullable=False)
    subject = db.Column(db.String(40), unique=False, nullable=False)
    message = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.name
