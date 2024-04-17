from app import app, db
from flask import render_template, flash, redirect, \
                url_for, request, abort, jsonify
import sqlalchemy as sa
from sqlalchemy.orm import joinedload
import app.models as models
from app.models import Ingredient, Dish, Order, DishInformation, \
                    OrderInformation, Customer, SupplyInfo, SupplyOrder
from app.forms import CreateDishForm, CreateOrderForm, CreateSupplyOrderForm, IngredientForm, \
                    IngredientForm2, ReportTwoForm, ReportOneForm, ReportThreeForm

from datetime import datetime

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    dishes = db.session.query(Dish).all()
    ingredients = db.session.query(Ingredient).all()
    orders = db.session.query(Order).all()
    
    return render_template('index.html', title="Restaurant System", dishes=dishes, 
                           ingredients=ingredients, orders=orders)


@app.route('/create_dishes', methods=['GET', 'POST'])
def form_dishes():
    ingredients = db.session.query(Ingredient).all()

    form = CreateDishForm()
    template_form = IngredientForm2(prefix='ingredient-_-')

    choices = [item.name for item in ingredients if item.quantity > 0]
    template_form.ingredient.choices = [item.name for item in ingredients if item.quantity > 0]
    for entry in form.ingredients.entries:
        entry.ingredient.choices = [item.name for item in ingredients if item.quantity > 0]

    if form.validate_on_submit():
        dish = Dish(name=form.name.data, price=form.price.data)
        db.session.add(dish)
        db.session.commit()
        
        for entry in form.ingredients.data:
            ingr_name = entry['ingredient']
            quantity_int = entry['quantity']
            if ingr_name in choices:
                ingr_id = [ing for ing in ingredients if ing.name == ingr_name][0].id
                dish_info = DishInformation(dish_id=dish.id, ingredient_id=ingr_id, quantity=quantity_int)
                db.session.add(dish_info)

        db.session.commit()
        flash(f"Created dish - {dish.name} with ingredients {[obj['ingredient'] for obj in form.ingredients.data]} for {dish.price} PLN")
        return redirect(url_for('form_dishes'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "error")

    return render_template('form_dish.html', title="Create dish", form=form, _template=template_form)


@app.route('/create_orders', methods=['GET', 'POST'])
def form_orders():
    dishes = db.session.query(Dish).all()
    
    form = CreateOrderForm()
    
    form.dishes.choices = [dish.name for dish in dishes]
    
    if form.validate_on_submit():
        price = 0.0
        try_customer = db.session.query(models.Customer).filter_by(card_number=form.card_number.data).first()
        if try_customer:
            try_customer.visits_number += 1
        else:
            try_customer = Customer(card_number=form.card_number.data, visits_number=1)
            db.session.add(try_customer)
            db.session.commit()

        order = Order(name=form.name.data, customer_id=try_customer.id)
        db.session.add(order)
        db.session.commit()
        for dish in form.dishes.data:
            try:
                db_dish = db.session.query(Dish).where(Dish.name == dish).first()
            except Exception:
                abort(404)

            price += db_dish.price
            
            for dish_info in db_dish.ingredients:
                db_ingredient = db.session.query(Ingredient).where(Ingredient.id == dish_info.ingredient_id).first()

                substract_val = db_ingredient.quantity - dish_info.quantity
                if substract_val <= 0:
                    flash(f'Could not create order for dish {dish}. Too few {db_ingredient.name}. Order more.')
                    return redirect(url_for('form_orders'))
                
                db_ingredient.quantity -= dish_info.quantity

                if db_ingredient.quantity < 3: # the average threshold
                    flash(f'You are running out of {db_ingredient.name}, there is only {db_ingredient.quantity} left.')
        
            new_order_info = OrderInformation(dish_id=db_dish.id, order_id=order.id)
            db.session.add(new_order_info)
    
        order.price = price
        db.session.commit()
        flash(f'Created order {order}. The price of the order is {price} PLN')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "error")

    return render_template('form_order.html', form=form)

@app.route('/supply_orders', methods=['GET', 'POST'])
def form_supply_order():
    form = CreateSupplyOrderForm()
    template_form = IngredientForm(prefix='ingredient-_-')

    ingredients = models.Ingredient.query.all()
    suppliers = models.Supplier.query.all()
    
    form.supplier_name.choices = [i.name for i in suppliers]

    if form.validate_on_submit():
        db_supplier = db.session.query(models.Supplier).filter_by(name=form.supplier_name.data).first()
        if db_supplier is None:
            abort(404)
        
        supply_order = models.SupplyOrder(supplier_id=db_supplier.id, price=0.0)
        db.session.add(supply_order)
        db.session.commit()
        
        price = 0.0
        for entry in form.ingredients.data:
            ingredient_name = entry['ingredient']
            quantity_int = entry['quantity']

            db_ingredient =  db.session.query(Ingredient).filter_by(name=ingredient_name).first()
            if db_ingredient is None:
                db_ingredient = Ingredient(name=ingredient_name, quantity=0, price=0.0)
                db.session.add(db_ingredient)
                db.session.commit()
            price += db_ingredient.price
            supply_info = models.SupplyInfo(ingredient_id=db_ingredient.id, 
                                            supply_order_id=supply_order.id, 
                                            quantity=quantity_int)
            db.session.add(supply_info)
        supply_order.price = price
        db.session.add(supply_order)
        db.session.commit()
        flash(f"Created supply order form for {[(obj['ingredient'], obj['quantity']) for obj in form.ingredients.data]}")

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "error")

    return render_template('supply_order.html', form=form, ingredients=ingredients, _template=template_form)

@app.route('/report1', methods=['GET', 'POST'])
def report_one():
    form = ReportOneForm()

    page = request.args.get('page', default=1, type=int)

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        orders = Order.query.options(joinedload(Order.customer)). \
                filter(Order.created_at.between(start_date, end_date)) \
                .order_by(Order.created_at)
        daily_totals = db.session.query(sa.func.date(Order.created_at), sa.func.sum(Order.price)).\
            filter(Order.created_at.between(start_date, end_date)).\
            group_by(sa.func.date(Order.created_at)).all()

        pagination = orders.paginate(page=page, per_page=300)
        
        if not pagination.items:
            flash("Empty report. Try different data.")
            return render_template('report1.html', pagination=pagination, 
                               start_date=start_date, end_date=end_date, 
                               form=form, daily_totals=daily_totals)

        flash("Check your reports's details")
        return render_template('report1.html', pagination=pagination, 
                               start_date=start_date, end_date=end_date, 
                               form=form, daily_totals=daily_totals)

    return render_template('report1.html', form=form, pagination=False)

@app.route('/report2', methods=['GET', 'POST'])
def report_two():
    form = ReportTwoForm()
    orders = Order.query.all()
    order_names = [order.name for order in orders]
    form.order_name.choices = order_names

    if form.validate_on_submit():
        try:
            db_order = db.session.query(Order).filter_by(name=form.order_name.data).first()
        except Exception:
            flash("Could not find the order")
            return render_template('report2.html', form=form)

        dishes = []
        dish_infos = db.session.query(OrderInformation).filter_by(order_id=db_order.id).all()
        for dish_info in dish_infos:
            d = Dish.query.get(dish_info.dish_id)
            dishes.append(d)
        
        customer = db.session.query(Customer).filter_by(id=db_order.customer_id).first()

        flash("Check your reports's details")
        return render_template('report2.html', order=db_order, customer=customer, dishes=dishes, form=form)

    return render_template('report2.html', form=form)


@app.route('/report3', methods=['GET', 'POST'])
def report_three():
    form = ReportThreeForm()
    
    if form.validate_on_submit():
        month = form.month.data
        year = form.year.data

        if not (1990 <= year <= datetime.now().year):
            abort(403)

        results = db.session.query(Ingredient.name, sa.func.sum(SupplyInfo.quantity), sa.func.sum(SupplyOrder.price)).\
            join(SupplyInfo, Ingredient.id == SupplyInfo.ingredient_id).\
            join(SupplyOrder, SupplyInfo.supply_order_id == SupplyOrder.id).\
            filter(sa.func.extract('month', SupplyOrder.created_at) == month).\
            filter(sa.func.extract('year', SupplyOrder.created_at) == year).\
            group_by(Ingredient.name).all()
        
        if len(results) == 0:
            flash("Empty report. Select different month")
        else:
            flash("Check your reports's details")
        return render_template('report3.html', data_ready=True, month=month, year=year, results=results, form=form)

    return render_template('report3.html', data_ready=False, form=form)


@app.route('/test_data') # TO BE REMOVED
def create_data():
    test_list = [
        Ingredient(name='bread', quantity=30, price=3.9),
        Ingredient(name='tomato sauce', quantity=3, price=10),
        Ingredient(name='pasta', quantity=9, price=10),
        Ingredient(name='mushrooms', quantity=6, price=9),
        Ingredient(name='coffee', quantity=20, price=5),
        Ingredient(name='milk', quantity=20, price=4),
        Ingredient(name='tomato sauce4', quantity=2, price=11)
    ]

    for elem in test_list:
        db.session.add(elem)

    # db.session.commit()
    # test_list = [
    #     Customer(card_number='1111-1111-1111-1111'),
    #     Customer(card_number='2222-2222-2222-2222'),
    #     Customer(card_number='3333-3333-3333-3333')
    # ]

    test_list = [
        models.Supplier(name='Tesco', address='Kwiatkowa Street 21'),
        models.Supplier(name='Kaufland', address='Drzewna Street 1'),
        models.Supplier(name='Carrefour', address='Krakowska Street 10/4')
    ]

    for elem in test_list:
        db.session.add(elem)

    db.session.commit()
    
    return {"ok": f"{test_list}"}