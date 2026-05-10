from __future__ import annotations

from datetime import date, datetime, timedelta

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from .. import db
from ..models import UserConsumption, UserMeal

nutrition_history = Blueprint("nutrition_history", __name__)


@nutrition_history.route("/nutrition-graphs")
@login_required
def nutrition_graphs():
    return render_template("nutrition_graphs.html", user=current_user)


@nutrition_history.route("/get-consumption-data", methods=["POST"])
@login_required
def get_consumption_data():
    data = request.get_json(silent=True) or {}

    if "start_date" not in data or "end_date" not in data:
        return jsonify({"error": "Start date and end date are required."}), 400

    try:
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if start_date > end_date:
        return jsonify({"error": "Start date cannot be after end date."}), 400

    today = date.today()
    if start_date > today or end_date > today:
        return jsonify({"error": "Dates cannot be in the future."}), 400

    if (end_date - start_date) > timedelta(days=365):
        return jsonify({"error": "Date range cannot exceed one year."}), 400

    consumptions = (
        UserConsumption.query.filter(
            UserConsumption.user_id == current_user.id,
            db.func.date(UserConsumption.timestamp) >= start_date,
            db.func.date(UserConsumption.timestamp) <= end_date,
        )
        .order_by(UserConsumption.timestamp.asc())
        .all()
    )

    aggregated_data = {}

    for consumption in consumptions:
        date_str = consumption.timestamp.strftime("%Y-%m-%d")
        aggregated_data.setdefault(date_str, {"calories": 0, "carbs": 0, "proteins": 0, "fats": 0})

        meal = db.session.get(UserMeal, consumption.meal_id)
        if not meal:
            continue

        quantity = consumption.quantity or 0

        aggregated_data[date_str]["calories"] += meal.calories * quantity / 100
        aggregated_data[date_str]["carbs"] += meal.carbs * quantity / 100
        aggregated_data[date_str]["proteins"] += meal.proteins * quantity / 100
        aggregated_data[date_str]["fats"] += meal.fats * quantity / 100

    chart_data = [
        {"date": date_str, **values}
        for date_str, values in sorted(aggregated_data.items())
    ]

    if not chart_data:
        return jsonify({"error": "No data available for the selected date range."}), 200

    return jsonify(chart_data)
