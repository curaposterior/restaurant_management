from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

import datetime

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128), unique=True)
    role = db.Column(db.String(10))


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    visits_number = db.Column(db.Integer)
    card_number = db.Column(db.String(19))

    orders = db.relationship('Order', backref='customer', lazy=True)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Datetime, default=datetime.datetime.utcnow)
    price = db.Column(db.Float)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_information_id = db.Column(db.Integer, db.ForeignKey('orderinformation.id'), nullable=False)


class OrderInformation(db.Model):
    __tablename__ = 'orderinformation'
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)


class Dish(db.Model):
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    price = db.Column(db.Integer)
    dish_information_id = db.Column(db.Integer, db.ForeignKey('dishinformation.id'), nullable=False)

    dish_information = db.relationship('DishInformation', backref='dish', nullable=False)


class DishInformation(db.Model):
    __tablename__ = 'dishinformation'
    id = db.Column(db.Integer, primary_key=True)

    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    dishes = db.relationship('DishInformation', backref='ingredients', lazy=True)


class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    address = db.Column(db.String(15))

    supply_orders = db.relationship('SupplyOrder', backref='supplier', lazy=True)


class SupplyOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Datetime)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
