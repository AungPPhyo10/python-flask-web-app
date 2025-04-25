from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())     # Date and time when the note was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # Foreign key to link the note to a user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    notes = db.relationship('Note')   # One to many relationship with Note
    tasks = db.relationship('Task')   # One to many relationship with Task

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))  
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())     # Date and time when the task was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # Foreign key to link the task to a user