from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from .. import db
from ..models import UserMeal

nutrition_management = Blueprint("nutrition_management", __name__)


def _parse_float(value, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a number") from error

    if parsed < 0:
        raise ValueError(f"{field_name} must be non-negative")

    return parsed


@nutrition_management.route("/add-meal", methods=["POST"])
@login_required
def add_meal():
    data = request.get_json(silent=True) or {}

    meal_name = (data.get("mealName") or "").strip()

    if not meal_name:
        return jsonify({"error": "Meal name is required."}), 400

    existing_meal = UserMeal.query.filter_by(name=meal_name, user_id=current_user.id).first()
    if existing_meal:
        return jsonify({"error": "A meal with this name already exists."}), 400

    try:
        new_meal = UserMeal(
            name=meal_name,
            calories=_parse_float(data.get("calories"), "Calories"),
            carbs=_parse_float(data.get("carbs"), "Carbs"),
            proteins=_parse_float(data.get("proteins"), "Proteins"),
            fats=_parse_float(data.get("fats"), "Fats"),
            user_id=current_user.id,
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"success": "Meal added successfully."}), 201


@nutrition_management.route("/delete-meal/<int:meal_id>", methods=["POST"])
@login_required
def delete_meal(meal_id):
    meal = db.session.get(UserMeal, meal_id)

    if meal is None or meal.user_id != current_user.id:
        return jsonify({"error": "Meal not found or permission denied."}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({"message": "Meal deleted successfully."})


@nutrition_management.route("/meals", methods=["GET"])
@login_required
def manage_meals():
    user_meals = UserMeal.query.filter_by(user_id=current_user.id).order_by(UserMeal.name.asc()).all()
    return render_template("meals.html", user=current_user, user_meals=user_meals)


@nutrition_management.route("/search-meals", methods=["GET"])
@login_required
def search_meals():
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify([])

    matching_meals = (
        UserMeal.query.filter(UserMeal.name.ilike(f"%{query}%"), UserMeal.user_id == current_user.id)
        .order_by(UserMeal.name.asc())
        .limit(30)
        .all()
    )

    return jsonify(
        [
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
    )
