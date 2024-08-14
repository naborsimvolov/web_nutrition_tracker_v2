from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from .home import home
    from .auth.auth import auth
    from .nutrition.nutrition_managment import nutrition_management
    from .nutrition.nutrition_history import nutrition_get_history
    from .nutrition.nutrition_calculate import nutrition_calculate
    from .user.user_page import user_profile
    from .models import User, UserMeal

    app.register_blueprint(user_profile, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(nutrition_calculate, url_prefix='/')
    app.register_blueprint(nutrition_management, url_prefix='/')
    app.register_blueprint(nutrition_get_history, url_prefix='/')


    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
