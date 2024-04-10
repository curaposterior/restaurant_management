from app import app, db
from flask import render_template, flash, redirect, url_for, request

import sqlalchemy as sa
from app.models import Ingredient, Dish, Order, DishInformation

from app.forms import CreateDishForm

@app.route('/')
@app.route('/index', methods=['GET'])
def index():

    return render_template('index.html', title="DBMS - Test")


@app.route('/create_ingredients')
def form_ingredients():

    return render_template('forms.html')


@app.route('/create_dishes', methods=['GET', 'POST'])
def form_dishes():
    ingredients = db.session.query(Ingredient).all()

    test_list = [
        Ingredient(id=1, name='bread', quantity=30, price=3.9),
        Ingredient(id=2, name='tomato sauce1', quantity=3, price=10),
        Ingredient(id=3, name='tomato sauce2', quantity=9, price=10),
        Ingredient(id=4, name='tomato sauce3', quantity=6, price=9),
        Ingredient(id=5, name='tomato sauce4', quantity=2, price=11)
    ]
    # form = CreateDishForm(data={"ingredients": test_list})
    form = CreateDishForm()
    # form.ingredients.query = test_list
    form.ingredients.choices = [(item.id, item.name) for item in test_list]
    if form.validate_on_submit():
        # create dish
        dish = Dish(name=form.name.data, price=form.price.data)
        for ingr in form.ingredients.data:
            print(type(ingr))

        # db.session.add(dish)
        # db.session.commit()
        flash(f"Created dish - {form.data}")
        

    return render_template('form_dish.html', title="Create dish", form=form)


@app.route('/create_orders')
def form_orders():

    return render_template('form_order.html')

@app.route('/supply_orders')
def form_supply_order():
    
    return render_template('supply_order.html')