from datetime import datetime
from flask_login import UserMixin
from . import db

from sqlalchemy import ForeignKey


class User(UserMixin,  db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.username


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))

    def __str__(self):
        return self.name


tagged_items = db.Table('tagged_items',
                        db.Column('tag_id', db.Integer,
                                  db.ForeignKey('tag.id')),
                        db.Column('question_id', db.Integer, db.ForeignKey('question.id')))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    details = db.Column(db.Text, nullable=True)
    asked = db.Column(db.DateTime, default=datetime.utcnow)
    # This field(updated) will be given value only when it is updated
    updated = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
                                                  ondelete='CASCADE',
                                                  onupdate='CASCADE'),
                        nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
    tags = db.relationship('Tag', secondary=tagged_items,
                           backref=db.backref('questions', lazy=True))

    def __str__(self):
        return self.title


class QuestionViews(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
                                                  ondelete='CASCADE',
                                                  onupdate='CASCADE'),
                        primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id',
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE'),
                            primary_key=True)
    user = db.relationship(
        'User', backref=db.backref('views', lazy=True))
    question = db.relationship(
        'Question', backref=db.backref('times_viewed', lazy=True))
