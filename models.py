from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class Member(UserMixin, db.Model):
    __tablename__ = 'Member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False, default=datetime.now)
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


class Good(db.Model):
    __tablename__ = 'Good'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    type_id = db.Column(db.Integer, db.ForeignKey('GoodType.id'))
    type = db.relationship('GoodType', backref='goods')
    author_id = db.Column(db.Integer, db.ForeignKey('Member.id'))
    author = db.relationship('Member', backref='goods')
    description = db.Column(db.Text, nullable=False, default='')


class GoodType(db.Model):
    __tablename__ = 'GoodType'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    size = db.Column(db.String(5), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(10), nullable=False)


class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
    amount = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    purchaser_id = db.Column(db.Integer, db.ForeignKey('Member.id'))
    purchaser = db.relationship('Member', backref='orders')


class OrderItem(db.Model):
    __tablename__ = 'OrderItem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    order = db.relationship('Order', backref='items')
    good_id = db.Column(db.Integer, db.ForeignKey('Good.id'))
    good = db.relationship('Good', backref='ref_orders')


class Rating(db.Model):
    __tablename__ = 'Rating'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(128), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    for_order_item_id = db.Column(db.Integer, db.ForeignKey('OrderItem.id'))
    for_order_item = db.relationship('OrderItem', uselist=False, backref=db.backref('rating', uselist=False))
    author_id = db.Column(db.Integer, db.ForeignKey('Member.id'))
    author = db.relationship('Member', backref='made_ratings')
