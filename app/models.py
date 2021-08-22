from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy as sa
from datetime import datetime


class IdModel(Model):
    id = sa.Column(sa.Integer, primary_key=True)


db = SQLAlchemy(model_class=IdModel)


class Client(db.Model):
    __tablename__ = 'clients'
    full_name = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(6), nullable=False)
    district = db.Column(db.String(50), nullable=False)


class Status(db.Model):
    __tablename__ = 'status'
    code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Product(db.Model):
    __tablename__ = 'products'
    name = db.Column(db.String(150), nullable=False)
    photo_url = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float(precision='7,2'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Role(db.Model):
    __tablename__ = 'roles'
    code = db.Column(db.String(15), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Users(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    status_id = db.Column(
        db.Integer,
        db.ForeignKey('status.id'),
        nullable=False
    )
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id'),
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class OrderProduct(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    note = db.Column(db.Text)
