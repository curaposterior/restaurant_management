from app import app, db
from flask import render_template, flash, redirect, url_for, request

import sqlalchemy as sa
from app.models import Ingredient, Dish, Order, DishInformation, \
                    OrderInformation
                       

from app.forms import CreateDishForm, CreateOrderForm

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
    
    form = CreateDishForm()
    choices = [item.name for item in ingredients]
    form.ingredients.choices = [item.name for item in ingredients]
    if form.validate_on_submit():
        # create dishs
        dish = Dish(name=form.name.data, price=form.price.data)
        db.session.add(dish)
        db.session.commit()
        
        for ingr in form.ingredients.data:
            if ingr in choices:
                ingr_id = [ing for ing in ingredients if ing.name == ingr][0].id
                dish_info = DishInformation(dish_id=dish.id, ingredient_id=ingr_id)
                db.session.add(dish_info)

        db.session.commit()
        flash(f"Created dish - {dish.name} with ingredients {form.ingredients.data}")
        return redirect(url_for('form_dishes'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "error")

    return render_template('form_dish.html', title="Create dish", form=form)


@app.route('/create_orders')
def form_orders():
    dishes = db.session.query(Dish).all()
    
    form = CreateOrderForm()
    form.dishes.choices = [dish.name for dish in dishes]
    if form.validate_on_submit():
        order = Order()
        for dish in form.dishes.data:
            pass
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "error")

    return render_template('form_order.html', form=form)

@app.route('/supply_orders')
def form_supply_order():
    
    return render_template('supply_order.html')

@app.route('/test_ingredients')
def create_data():
    test_list = [
        Ingredient(name='bread', quantity=30, price=3.9),
        Ingredient(name='tomato sauce1', quantity=3, price=10),
        Ingredient(name='tomato sauce2', quantity=9, price=10),
        Ingredient(name='tomato sauce3', quantity=6, price=9),
        Ingredient(name='tomato sauce4', quantity=2, price=11)
    ]

    for elem in test_list:
        db.session.add(elem)
    
    db.session.commit()
    
    return {"ok": "ok"}