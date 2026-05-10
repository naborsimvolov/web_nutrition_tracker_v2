from __future__ import annotations

import json
from datetime import datetime

from flask import current_app
from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)

    daily_calories_goal = db.Column(db.Float, default=2000.0)
    daily_carbs_goal = db.Column(db.Float, default=275.0)
    daily_proteins_goal = db.Column(db.Float, default=50.0)
    daily_fats_goal = db.Column(db.Float, default=70.0)

    meals = db.relationship("UserMeal", backref="user", lazy=True, cascade="all, delete-orphan")

    def populate_default_meals_from_json(self) -> None:
        """Populate a new user's meal database from instance/default_database.json."""
        default_meals_path = current_app.config["DEFAULT_MEALS_PATH"]

        with open(default_meals_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            meal = UserMeal(
                name=item["food name"],
                calories=float(item["kilocalories"]),
                carbs=float(item["carbohydrates"]),
                proteins=float(item["proteins"]),
                fats=float(item["fats"]),
                user_id=self.id,
            )
            db.session.add(meal)

        db.session.commit()


class UserMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class UserConsumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey("user_meal.id"), nullable=False)
    quantity = db.Column(db.Float, default=0.0, nullable=False)

    meal = db.relationship("UserMeal", backref="consumptions")


class DailyGoalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=lambda: datetime.utcnow().date(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    calories_goal = db.Column(db.Float, nullable=False)
    carbs_goal = db.Column(db.Float, nullable=False)
    proteins_goal = db.Column(db.Float, nullable=False)
    fats_goal = db.Column(db.Float, nullable=False)


def update_user_goals(user: User, calories_goal: float, carbs_goal: float, proteins_goal: float, fats_goal: float) -> None:
    user.daily_calories_goal = calories_goal
    user.daily_carbs_goal = carbs_goal
    user.daily_proteins_goal = proteins_goal
    user.daily_fats_goal = fats_goal

    history_entry = DailyGoalHistory(
        user_id=user.id,
        calories_goal=calories_goal,
        carbs_goal=carbs_goal,
        proteins_goal=proteins_goal,
        fats_goal=fats_goal,
    )

    db.session.add(history_entry)
    db.session.commit()
