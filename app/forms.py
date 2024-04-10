from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms import StringField, PasswordField, BooleanField, \
            SubmitField, IntegerField, FloatField, SelectMultipleField
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
    
    