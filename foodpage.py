from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import UserMeal
from . import db

views = Blueprint('foodpage', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and 'action' in request.form:
        action = request.form.get('action')

        if action == 'add_meal':

            meal_name = request.form.get('mealName').strip()
            carbs = request.form.get('carbs')
            proteins = request.form.get('proteins')
            fats = request.form.get('fats')


            existing_meal = UserMeal.query.filter_by(name=meal_name, user_id=current_user.id).first()
            if existing_meal:
                flash('A meal with this name already exists. Please use a different name.', category='error')
            else:

                if meal_name and carbs != '' and proteins != '' and fats != '':
                    try:
                        carbs = float(carbs)
                        proteins = float(proteins)
                        fats = float(fats)

                        new_meal = UserMeal(name=meal_name, carbs=carbs, proteins=proteins, fats=fats,
                                            user_id=current_user.id)
                        db.session.add(new_meal)
                        db.session.commit()
                        flash('Meal added!', category='success')
                    except ValueError:
                        flash('Please enter valid numbers for carbs, proteins, and fats.', category='error')
                else:
                    flash('All fields are required to add a new meal.', category='error')
    user_meals = UserMeal.query.filter_by(user_id=current_user.id).all()
    consumed_totals = session.get('consumed_totals', {})
    return render_template("home.html", user=current_user, user_meals=user_meals, consumed_totals=consumed_totals)

@views.route('/delete-meal', methods=['POST'])
@login_required
def delete_meal():
    meal_id = request.form.get('mealId')
    meal = UserMeal.query.get(meal_id)
    if meal and meal.user_id == current_user.id:
        db.session.delete(meal)
        db.session.commit()
        flash('Meal deleted!', category='success')
    else:
        flash('Meal not found or you do not have permission to delete this meal.', category='error')
    return redirect(url_for('foodpage.home'))

@views.route('/suggest-meals')
def suggest_meals():
    query = request.args.get('query', '')
    matching_meals = UserMeal.query.filter(
        UserMeal.name.like(f'%{query}%'),
        UserMeal.user_id == current_user.id
    ).all()

    meals_data = [{
        'name': meal.name,
        'carbs': meal.carbs,
        'proteins': meal.proteins,
        'fats': meal.fats
    } for meal in matching_meals]

    return jsonify(meals_data)



@views.route('/nutrition-graphs')
@login_required
def nutrition_graphs():
    return render_template("nutrition_graphs.html")