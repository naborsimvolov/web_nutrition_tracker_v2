from . import db
from flask_login import UserMixin
import json
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    meals = db.relationship('UserMeal', backref='user', lazy=True)

    def populate_default_meals_from_json(self, json_file_path):
        # Open and read the JSON file
        with open("instance/default_database.json", 'r') as file:
            data = json.load(file)

        # Iterate over each food item in the JSON data
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

        # Commit the session to save all meals to the database
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

