from flask_login import UserMixin
from . import db


class User(UserMixin,  db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.email