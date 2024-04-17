from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms import StringField, \
            SubmitField, IntegerField, FloatField, SelectMultipleField, \
            SelectField, FormField, FieldList, Form, DateField

import wtforms.validators as validators
from wtforms.validators import DataRequired

import calendar


class IngredientForm(Form):
    ingredient = StringField('Ingredient', validators=[validators.DataRequired(), validators.Length(max=100)])
    quantity = IntegerField('Quantity', validators=[validators.DataRequired()])


class IngredientForm2(Form):
    ingredient = SelectField('Select ingredient', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class CreateDishForm(FlaskForm):
    name = StringField('Dish name', validators=[DataRequired()])
    price = FloatField('Price of the dish', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm2), min_entries=1, max_entries=20)
    
class CreateOrderForm(FlaskForm):
    name = StringField('Order name (e.g. table number)', validators=[DataRequired()])
    card_number = StringField('Credit card number', validators=[DataRequired()])
    dishes = SelectMultipleField('Dishes (press ctrl to select more)', validators=[DataRequired()])


class CreateSupplyOrderForm(FlaskForm):
    ingredients = FieldList(FormField(IngredientForm), min_entries=1, max_entries=10)
    supplier_name = SelectField('Select supplier', validators=[DataRequired()])


class ReportOneForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Generate Report')


class ReportTwoForm(FlaskForm):
    order_name = SelectField('Select order by name', validators=[DataRequired()])


class ReportThreeForm(FlaskForm):
    month = SelectField('Month', 
                        choices=[(i, calendar.month_name[i]) for i in range(1,13)], 
                        validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
