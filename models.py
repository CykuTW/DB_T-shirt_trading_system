from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    phone = db.Column(db.String(15), nullable=False)
    permission = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self):
        super().__init__()

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.permission & 0x1 != 0
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)