from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone

import datetime

from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    role: so.Mapped[str] = so.mapped_column(sa.String(20))

    def __repr__(self):
        return '<User {}:{}>'.format(self.email, self.role)


class Customer(db.Model):
    __tablename__ = 'customer'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    visits_number: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    card_number: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    orders: so.WriteOnlyMapped['Order'] = so.relationship('Order', backref='customer')


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(20))
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer)
    price: so.Mapped[float] = so.mapped_column(sa.Float)

    # dishes: so.WriteOnlyMapped['Dish'] = so.relationship(back_populates='dish')

    def __repr__(self) -> str:
        return f"{self.id}. {self.name}"


class DishInformation(db.Model):
    __tablename__ = 'dish_information'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    dish_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('dish.id'))
    ingredient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('ingredient.id'))
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, default=1)


class Dish(db.Model):
    __tablename__ = 'dish'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True)
    price: so.Mapped[float] = so.mapped_column(sa.Float)

    # dish_information_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('dish_information.id'))
    ingredients = db.relationship('DishInformation', backref='dish', foreign_keys='DishInformation.dish_id')


class OrderInformation(db.Model):
    __tablename__ = "order_information"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    dish_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('dish.id'))
    order_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('order.id'))
    # quantity: so.Mapped[int] = so.mapped_column(sa.Integer)


class Order(db.Model):
    __tablename__ = 'order'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(30), unique=True)
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        default=lambda: datetime.datetime.now())
    price: so.Mapped[float] = so.mapped_column(sa.Float, default=0.0)
    
    customer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Customer.id), index=True)


class Supplier(db.Model):
    __tablename__ = 'supplier'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(15))
    address: so.Mapped[str] = so.mapped_column(sa.String(15))


class SupplyOrder(db.Model):
    __tablename__ = 'supply_order'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # quantity: so.Mapped[int] = so.mapped_column(sa.Integer)
    price: so.Mapped[int] = so.mapped_column(sa.Float)
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(default=lambda: datetime.datetime.now())
    
    supplier_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('supplier.id'))


class SupplyInfo(db.Model):
    __tablename__ = 'supply_info'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    ingredient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('ingredient.id'))
    supply_order_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('supply_order.id'))
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, default=1)
