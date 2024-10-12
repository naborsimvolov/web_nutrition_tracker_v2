from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..models import UserConsumption, UserMeal
from .. import db
from datetime import datetime, timedelta, date

nutrition_history = Blueprint('nutrition_history', __name__)

@nutrition_history.route('/nutrition-graphs')
@login_required
def nutrition_graphs():
    return render_template('nutrition_graphs.html', user=current_user)

@nutrition_history.route('/get-consumption-data', methods=['POST'])
@login_required
def get_consumption_data():
    data = request.get_json()
    # if start_date and end_date are provided
    if not data or 'start_date' not in data or 'end_date' not in data:
        return jsonify({'error': 'Start date and end date are required.'}), 400
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    # tart_date
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid start date format. Use YYYY-MM-DD.'}), 400
    # end_date
    try:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid end date format. Use YYYY-MM-DD.'}), 400

    # validate
    if start_date > end_date:
        return jsonify({'error': 'Start date cannot be after end date.'}), 400

    # if dates are not in future
    today = date.today()
    if start_date > today or end_date > today:
        return jsonify({'error': 'Dates cannot be in the future.'}), 400

    # max of 1 year
    max_date_range = timedelta(days=365)
    if (end_date - start_date) > max_date_range:
        return jsonify({'error': 'Date range cannot exceed one year.'}), 400
    # consumption data
    try:
        consumptions = UserConsumption.query.filter(
            UserConsumption.user_id == current_user.id,
            db.func.date(UserConsumption.timestamp) >= start_date,
            db.func.date(UserConsumption.timestamp) <= end_date
        ).all()
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching data.'}), 500
    # agr data
    aggregated_data = {}
    for consumption in consumptions:
        date_str = consumption.timestamp.strftime('%Y-%m-%d')
        if date_str not in aggregated_data:
            aggregated_data[date_str] = {'calories': 0, 'carbs': 0, 'proteins': 0, 'fats': 0}
        meal = UserMeal.query.get(consumption.meal_id)
        if meal:
            quantity = consumption.quantity or 1  # def to 1 if quantity is zero
            aggregated_data[date_str]['calories'] += meal.calories * quantity
            aggregated_data[date_str]['carbs'] += meal.carbs * quantity
            aggregated_data[date_str]['proteins'] += meal.proteins * quantity
            aggregated_data[date_str]['fats'] += meal.fats * quantity
    # prep data for chart
    chart_data = []
    for date_str in sorted(aggregated_data.keys()):
        data_point = {
            'date': date_str,
            'calories': aggregated_data[date_str]['calories'],
            'carbs': aggregated_data[date_str]['carbs'],
            'proteins': aggregated_data[date_str]['proteins'],
            'fats': aggregated_data[date_str]['fats'],
        }
        chart_data.append(data_point)
    if not chart_data:
        return jsonify({'error': 'No data available for the selected date range.'}), 200

    return jsonify(chart_data)