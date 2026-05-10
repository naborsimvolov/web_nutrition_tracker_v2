from __future__ import annotations

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object("website.config.Config")

    db.init_app(app)

    from .auth.auth import auth
    from .home import home
    from .models import User
    from .nutrition.nutrition_calculate import nutrition_calculate
    from .nutrition.nutrition_history import nutrition_history
    from .nutrition.nutrition_managment import nutrition_management
    from .user.user_page import user_profile

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user_profile)
    app.register_blueprint(nutrition_calculate)
    app.register_blueprint(nutrition_management)
    app.register_blueprint(nutrition_history)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    return app
