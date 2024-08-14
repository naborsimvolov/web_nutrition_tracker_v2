from flask import Blueprint, render_template, request, jsonify, session, flash
from flask_login import login_required, current_user
from ..models import UserMeal

nutrition_calculate = Blueprint('nutrition_calculate', __name__)

@nutrition_calculate.route('/calculate', methods=['GET', 'POST'])
@login_required
def calculate():
    if request.method == 'POST':
        meal_data = request.get_json().get('mealData')
        if not meal_data:
            flash('No meals data provided.', category='error')
            return jsonify({'error': 'No meals data provided.'}), 400

        return jsonify(meal_data)

    user_meals = UserMeal.query.filter_by(user_id=current_user.id).all()
    return render_template('calculate.html', user_meals=user_meals)



@nutrition_calculate.route('/suggest-meals')
def suggest_meals():
    query = request.args.get('query', '')
    matching_meals = UserMeal.query.filter(
        UserMeal.name.like(f'%{query}%'),
        UserMeal.user_id == current_user.id
    ).all()

    meals_data = [{
        'name': meal.name,
        'calories': meal.calories,
        'carbs': meal.carbs,
        'proteins': meal.proteins,
        'fats': meal.fats
    } for meal in matching_meals]

    return jsonify(meals_data)