from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func

from .. import db
from ..models import UserConsumption, UserMeal

nutrition_calculate = Blueprint("nutrition_calculate", __name__)


def _nutrition_totals_query():
    return db.session.query(
        func.sum(UserMeal.calories * UserConsumption.quantity / 100).label("total_calories"),
        func.sum(UserMeal.carbs * UserConsumption.quantity / 100).label("total_carbs"),
        func.sum(UserMeal.proteins * UserConsumption.quantity / 100).label("total_proteins"),
        func.sum(UserMeal.fats * UserConsumption.quantity / 100).label("total_fats"),
    ).select_from(UserConsumption).join(UserMeal, UserMeal.id == UserConsumption.meal_id)


@nutrition_calculate.route("/get-today-nutrition", methods=["GET"])
@login_required
def get_today_nutrition():
    today_consumption = (
        _nutrition_totals_query()
        .filter(
            UserConsumption.user_id == current_user.id,
            func.date(UserConsumption.timestamp) == func.current_date(),
        )
        .first()
    )

    return jsonify(
        {
            "total_calories": today_consumption.total_calories or 0,
            "total_carbs": today_consumption.total_carbs or 0,
            "total_proteins": today_consumption.total_proteins or 0,
            "total_fats": today_consumption.total_fats or 0,
        }
    )


@nutrition_calculate.route("/calculate", methods=["GET", "POST"])
@login_required
def calculate():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        meal_data = payload.get("mealData")

        if not meal_data:
            return jsonify({"error": "No meals data provided."}), 400

        for meal_entry in meal_data:
            meal_name = meal_entry.get("name")
            amount = float(meal_entry.get("amount") or 0)

            meal = UserMeal.query.filter_by(name=meal_name, user_id=current_user.id).first()
            if meal is None:
                return jsonify({"error": f"Meal not found: {meal_name}"}), 404
            if amount <= 0:
                return jsonify({"error": "Meal amount must be greater than zero."}), 400

            db.session.add(
                UserConsumption(
                    user_id=current_user.id,
                    meal_id=meal.id,
                    quantity=amount,
                )
            )

        db.session.commit()
        return jsonify({"message": "Consumption recorded successfully."})

    user_goals = {
        "calories": current_user.daily_calories_goal,
        "carbs": current_user.daily_carbs_goal,
        "proteins": current_user.daily_proteins_goal,
        "fats": current_user.daily_fats_goal,
    }

    return render_template("calculate.html", user_goals=user_goals, user=current_user)


@nutrition_calculate.route("/suggest-meals")
@login_required
def suggest_meals():
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify([])

    matching_meals = (
        UserMeal.query.filter(UserMeal.name.ilike(f"%{query}%"), UserMeal.user_id == current_user.id)
        .order_by(UserMeal.name.asc())
        .limit(20)
        .all()
    )

    meals_data = [
        {
            "id": meal.id,
            "name": meal.name,
            "calories": meal.calories,
            "carbs": meal.carbs,
            "proteins": meal.proteins,
            "fats": meal.fats,
        }
        for meal in matching_meals
    ]

    return jsonify(meals_data)
