from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    phone = db.Column(db.String(15), nullable=False)
    permission = db.Column(db.Integer, nullable=False, default=0)
