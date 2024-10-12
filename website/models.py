from . import db
from flask_login import UserMixin
import json
from datetime import datetime
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    meals = db.relationship('UserMeal', backref='user', lazy=True)

    daily_calories_goal = db.Column(db.Float, default=2000.0)
    daily_carbs_goal = db.Column(db.Float, default=275.0)
    daily_proteins_goal = db.Column(db.Float, default=50.0)
    daily_fats_goal = db.Column(db.Float, default=70.0)
    def populate_default_meals_from_json(self):
        # op and read the json file
        with open("/Users/alexander/PycharmProjects/web_nutrition_tracker_V1/instance/defualt_database.json", 'r') as file:
            data = json.load(file)
        # over each food item in json
        for item in data:
            meal = UserMeal(
                name=item['food name'],
                calories=int(item['kilocalories']),
                carbs=float(item['carbohydrates']),
                proteins=float(item['proteins']),
                fats=float(item['fats']),
                user_id=self.id
            )
            db.session.add(meal)
        # commit session to save all meals
        db.session.commit()

class UserMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    calories = db.Column(db.Integer)
    carbs = db.Column(db.Float)
    proteins = db.Column(db.Float)
    fats = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, calories, carbs, proteins, fats, user_id):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.proteins = proteins
        self.fats = fats
        self.user_id = user_id

class UserConsumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('user_meal.id'))
    quantity = db.Column(db.Float, default=0.0)
    meal = db.relationship('UserMeal', backref='consumptions')

    def __init__(self, user_id, meal_id, quantity):
        self.user_id = user_id
        self.meal_id = meal_id
        self.quantity = quantity
        self.timestamp = datetime.utcnow()

class DailyGoalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    calories_goal = db.Column(db.Float)
    carbs_goal = db.Column(db.Float)
    proteins_goal = db.Column(db.Float)
    fats_goal = db.Column(db.Float)

    def __init__(self, user_id, calories_goal, carbs_goal, proteins_goal, fats_goal):
        self.user_id = user_id
        self.calories_goal = calories_goal
        self.carbs_goal = carbs_goal
        self.proteins_goal = proteins_goal
        self.fats_goal = fats_goal
        self.date = datetime.utcnow().date()

#  update user goals
def update_user_goals(user, calories_goal, carbs_goal, proteins_goal, fats_goal):
    user.daily_calories_goal = calories_goal
    user.daily_carbs_goal = carbs_goal
    user.daily_proteins_goal = proteins_goal
    user.daily_fats_goal = fats_goal
    #save record of goal in history
    history_entry = DailyGoalHistory(
        user_id=user.id,
        calories_goal=calories_goal,
        carbs_goal=carbs_goal,
        proteins_goal=proteins_goal,
        fats_goal=fats_goal
    )
    db.session.add(history_entry)
    db.session.commit()