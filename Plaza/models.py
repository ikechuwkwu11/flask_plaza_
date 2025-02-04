from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    address = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Float, nullable = False)
    stock = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}' )"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

    user = db.relationship('User', backref=db.backref('carts', lazy = True))
    product = db.relationship('Product', backref = db.backref('carts', lazy = True))

    def __repr__(self):
        return f"Cart('{self.product.name}', '{self.quantity}')"


