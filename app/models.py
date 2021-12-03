from io import BytesIO
from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy as sa
from datetime import datetime
from flask_login import UserMixin
import base64
import requests
from config import Config
from flask import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class IdModel(Model):
    id = sa.Column(sa.Integer, primary_key=True)


db = SQLAlchemy(model_class=IdModel)


class Client(db.Model):
    __tablename__ = 'clients'
    full_name = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(6), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='client')


class Status(db.Model):
    __tablename__ = 'status'
    code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    products = db.relationship('Product', backref='category')


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
    users = db.relationship('User', backref='role')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_reset_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)


class Order(db.Model):
    __tablename__ = 'orders'
    status_id = db.Column(
        db.Integer,
        db.ForeignKey('status.id'),
        nullable=False
    )
    status = db.relationship('Status')
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id'),
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    note = db.Column(db.Text)
    products = db.relationship('OrderProduct', backref='order')
    txid = db.Column(db.String(35))
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
    __tablename__ = 'order_products'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product')
    quantity = db.Column(db.Integer)


class PixModel():
    def __init__(self) -> None:
        self.headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        auth = base64.b64encode(
            (f'{Config.PIX_CLIENT_ID}:{Config.PIX_SECRET}').encode()
        ).decode()

        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }

        payload = {'grant_type': 'client_credentials'}

        response = requests.post(
            f'{Config.PIX_URL}/oauth/token',
            headers=headers,
            data=json.dumps(payload),
            cert=Config.CERTIFICATE
        )

        return json.loads(response.content)['access_token']

    def create_qrcode(self, location_id):
        response = requests.get(
            f'{Config.PIX_URL}/v2/loc/{location_id}/qrcode',
            headers=self.headers,
            cert=Config.CERTIFICATE
        )

        return json.loads(response.content)

    def create_order(self, txid, payload):
        response = requests.put(
            f'{Config.PIX_URL}/v2/cob/{txid}',
            data=json.dumps(payload),
            headers=self.headers,
            cert=Config.CERTIFICATE
        )

        if response.status_code == 201:
            return json.loads(response.content)

        return {}

    def qrcode_gererator(self, location_id):
        qrcode = self.create_qrcode(location_id)

        return qrcode['imagemQrcode']

    def create_charge(self, txid, payload):
        location_id = self.create_order(txid, payload).get('loc').get('id')
        qrcode = self.qrcode_gererator(location_id)

        return qrcode
