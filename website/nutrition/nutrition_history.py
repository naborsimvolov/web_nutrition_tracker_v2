from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from ..models import UserMeal
from .. import db

nutrition_get_history = Blueprint('nutrition_views', __name__)

@nutrition_get_history.route('/nutrition-history')
@login_required
def get_nutrition_data():
    # Query all meals for the current user
    meals = UserMeal.query.filter_by(user_id=current_user.id).all()

    # Sum up the nutrients for all time
    total_carbs = sum(meal.carbs for meal in meals)
    total_proteins = sum(meal.proteins for meal in meals)
    total_fats = sum(meal.fats for meal in meals)
    total_calories = sum(meal.calories for meal in meals)  # Sum calories for all time

    return jsonify({
        'total_carbs': total_carbs,
        'total_proteins': total_proteins,
        'total_fats': total_fats,
        'total_calories': total_calories  # Include total calories in the response
    })
