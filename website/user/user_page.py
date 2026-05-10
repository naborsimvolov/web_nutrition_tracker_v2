from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from ..models import update_user_goals

user_profile = Blueprint("user_profile", __name__)


def _parse_positive_float(value, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a number") from error

    if parsed < 0:
        raise ValueError(f"{field_name} must be non-negative")

    return parsed


@user_profile.route("/profile")
@login_required
def profile():
    return render_template("userprofile.html", user=current_user)


@user_profile.route("/save-goals", methods=["POST"])
@login_required
def save_goals():
    data = request.get_json(silent=True) or {}

    try:
        update_user_goals(
            user=current_user,
            calories_goal=_parse_positive_float(data.get("calories"), "Calories goal"),
            carbs_goal=_parse_positive_float(data.get("carbs"), "Carbs goal"),
            proteins_goal=_parse_positive_float(data.get("proteins"), "Proteins goal"),
            fats_goal=_parse_positive_float(data.get("fats"), "Fats goal"),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"success": "Goals saved successfully."})
