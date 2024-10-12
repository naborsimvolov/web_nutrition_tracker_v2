from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..models import UserMeal
from .. import db

nutrition_management = Blueprint('nutrition_management', __name__)

@nutrition_management.route('/add-meal', methods=['POST'])
@login_required
def add_meal():
    try:
        data = request.get_json()
        meal_name = data.get('mealName')
        calories = data.get("calories")
        carbs = data.get('carbs')
        proteins = data.get('proteins')
        fats = data.get('fats')
        existing_meal = UserMeal.query.filter_by(name=meal_name, user_id=current_user.id).first()
        if existing_meal:
            return jsonify({'error': 'A meal with this name already exists. Please delete it first if you wish to overwrite it.'}), 400
        if meal_name and calories and carbs and proteins and fats:
            try:
                new_meal = UserMeal(
                    name=meal_name,
                    carbs=float(carbs),
                    proteins=float(proteins),
                    fats=float(fats),
                    calories=float(calories),
                    user_id=current_user.id
                )
                db.session.add(new_meal)
                db.session.commit()
                return jsonify({'success': 'Meal added successfully'}), 201
            except ValueError as e:
                return jsonify({'error': f'Error adding meal: {str(e)}'}), 400
        else:
            return jsonify({'error': 'All fields are required to add a new meal'}), 400
    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

@nutrition_management.route('/delete-meal/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):
    meal = UserMeal.query.get(meal_id)
    if meal and meal.user_id == current_user.id:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'message': 'Meal deleted successfully'}), 200
    else:
        return jsonify({'error': 'Meal not found or permission denied'}), 404

@nutrition_management.route('/meals', methods=['GET'])
@login_required
def manage_meals():
    user_meals = UserMeal.query.filter_by(user_id=current_user.id).all()
    return render_template('meals.html', user=current_user, user_meals=user_meals)

@nutrition_management.route('/search-meals', methods=['GET'])
@login_required
def search_meals():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    matching_meals = UserMeal.query.filter(
        UserMeal.name.ilike(f'%{query}%'),
        UserMeal.user_id == current_user.id
    ).all()

    meals_data = [{
        'id': meal.id,
        'name': meal.name,
        'calories': meal.calories,
        'carbs': meal.carbs,
        'proteins': meal.proteins,
        'fats': meal.fats
    } for meal in matching_meals]

    return jsonify(meals_data), 200