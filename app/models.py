from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy as sa
from datetime import datetime


class IdModel(Model):
    id = sa.Column(sa.Integer, primary_key=True)


db = SQLAlchemy(model_class=IdModel)


class Client(db.Model):
    __tablename__ = 'clients'
    full_name = db.Column(db.String(250))
    phone = db.Column(db.String(11))
    cpf = db.Column(db.String(11))
    street = db.Column(db.String(255))
    number = db.Column(db.String(6))
    district = db.Column(db.String(50))


class Status(db.Model):
    __tablename__ = 'status'
    code = db.Column(db.String(20))
    description = db.Column(db.Text)


class Category(db.Model):
    __tablename__ = 'categories'
    name = db.Column(db.String(20))
    description = db.Column(db.Text)


class Product(db.Model):
    __tablename__ = 'products'
    name = db.Column(db.String(150))
    photo_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float(precision='7,2'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Role(db.Model):
    __tablename__ = 'roles'
    code = db.Model(db.String(15))
    description = db.Model(db.Text)


class Users(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(255))
    username = db.Column(db.String(20))
    password = db.Column(db.String(255))


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Order(db.Model):
    __tablename__ = 'orders'
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
