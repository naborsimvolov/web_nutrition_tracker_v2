from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from ..models import UserMeal, UserConsumption, db
from sqlalchemy import func
nutrition_calculate = Blueprint('nutrition_calculate', __name__)

@nutrition_calculate.route('/get-today-nutrition', methods=['GET'])
@login_required
def get_today_nutrition():
    try:
        today_consumption = db.session.query(
            func.sum(UserMeal.calories * UserConsumption.quantity / 100).label('total_calories'),
            func.sum(UserMeal.carbs * UserConsumption.quantity / 100).label('total_carbs'),
            func.sum(UserMeal.proteins * UserConsumption.quantity / 100).label('total_proteins'),
            func.sum(UserMeal.fats * UserConsumption.quantity / 100).label('total_fats')
        ).select_from(UserConsumption).join(UserMeal, UserMeal.id == UserConsumption.meal_id
        ).filter(
            UserConsumption.user_id == current_user.id,
            func.date(UserConsumption.timestamp) == func.current_date()
        ).first()

        return jsonify({
            'total_calories': today_consumption.total_calories or 0,
            'total_carbs': today_consumption.total_carbs or 0,
            'total_proteins': today_consumption.total_proteins or 0,
            'total_fats': today_consumption.total_fats or 0
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutrition_calculate.route('/calculate', methods=['GET', 'POST'])
@login_required
def calculate():
    if request.method == 'POST':
        meal_data = request.get_json().get('mealData')
        if not meal_data:
            flash('No meals data provided.', category='error')
            return jsonify({'error': 'No meals data provided.'}), 400
        for meal_entry in meal_data:
            meal = UserMeal.query.filter_by(name=meal_entry['name'], user_id=current_user.id).first()
            consumption = UserConsumption(
                user_id=current_user.id,
                meal_id=meal.id,
                quantity=meal_entry['amount']
            )
            db.session.add(consumption)
        db.session.commit()
        return jsonify({'message': 'Consumption recorded and nutrition calculated successfully!'}), 200

    # user daily goals to frontend
    user_goals = {
        'calories': current_user.daily_calories_goal,
        'carbs': current_user.daily_carbs_goal,
        'proteins': current_user.daily_proteins_goal,
        'fats': current_user.daily_fats_goal
    }

    user_meals = UserMeal.query.filter_by(user_id=current_user.id).all()
    return render_template('calculate.html', user_meals=user_meals, user_goals=user_goals)
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