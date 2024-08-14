from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from ..models import UserMeal
from .. import db

nutrition_management = Blueprint('nutrition_management', __name__)

@nutrition_management.route('/meals', methods=['GET'])
@login_required
def manage_meals():
    user_meals = UserMeal.query.filter_by(user_id=current_user.id).all()
    return render_template('meals.html', user=current_user, user_meals=user_meals)

@nutrition_management.route('/add-meal', methods=['POST'])
@login_required
def add_meal():
    data = request.get_json()
    meal_name = data['mealName']
    calories = data["calories"]
    carbs = data['carbs']
    proteins = data['proteins']
    fats = data['fats']
    existing_meal = UserMeal.query.filter_by(name=meal_name, user_id=current_user.id).first()
    if existing_meal:
        return jsonify({'error': 'A meal with this name already exists'}), 400
        flash('A meal with this name already exists', category='error')
    else:
        # Proceed with adding the new meal if it doesn't already exist
        if meal_name and carbs != '' and proteins != '' and fats != '' and calories != '':
            try:
                new_meal = UserMeal(name=meal_name, carbs=float(carbs), proteins=float(proteins), fats=float(fats), calories=float(calories),
                                    user_id=current_user.id)
                db.session.add(new_meal)
                db.session.commit()
                return jsonify({'success': 'Meal added successfully'})
            except ValueError as e:
                return jsonify({'error': f'Error adding meal: {str(e)}'}), 400
                flash('Please enter valid numbers for carbs, proteins, and fats.', category='error')
        else:
            flash('All fields are required to add a new meal.', category='error')
    user_meals = UserMeal.query.filter_by(user_id=current_user.id).all()
    return render_template('meals.html',user=current_user, user_meals=user_meals)


@nutrition_management.route('/delete-meal/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):
    meal = UserMeal.query.get(meal_id)
    if meal and meal.user_id == current_user.id:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'message': 'Meal deleted successfully'})
    else:
        return jsonify({'error': 'Meal not found or permission denied'}), 404
