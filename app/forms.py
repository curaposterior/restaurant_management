from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms import StringField, PasswordField, BooleanField, \
            SubmitField, IntegerField, FloatField, SelectMultipleField, \
            SelectField, FormField, FieldList

from wtforms.validators import DataRequired

from wtforms_alchemy import QuerySelectMultipleField
from wtforms import widgets

class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CreateDishForm(FlaskForm):
    name = StringField('Dish name', validators=[DataRequired()])
    price = FloatField('Price of the dish', validators=[DataRequired()])
    # ingredients = QuerySelectMultipleFieldWithCheckboxes("Ingredients")
    ingredients = SelectMultipleField('Ingredients', validators=[DataRequired()])
    
class CreateOrderForm(FlaskForm):
    name = StringField('Order name (e.g. table number)', validators=[DataRequired()])
    card_number = StringField('Credit card number', validators=[DataRequired()])
    dishes = SelectMultipleField('Dishes (press ctrl to select more)', validators=[DataRequired()])



class IngredientForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class CreateSupplyOrderForm(FlaskForm):
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    supplier_name = SelectField('Select supplier', validators=[DataRequired()])
