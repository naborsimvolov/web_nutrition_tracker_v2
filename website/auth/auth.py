from __future__ import annotations

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from ..models import User

auth = Blueprint("auth", __name__)


def _normalize_email(email: str | None) -> str:
    return (email or "").lower().strip()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = _normalize_email(request.form.get("email"))
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({"success": True, "redirect": url_for("home.index")})

        return jsonify({"success": False, "message": "Incorrect email or password, please try again."}), 401

    return render_template("login.html", user=current_user)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = _normalize_email(request.form.get("email"))
        first_name = (request.form.get("firstName") or "").strip()
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Email already exists."}), 400
        if len(email) < 6 or "@" not in email:
            return jsonify({"success": False, "message": "Enter a valid email address."}), 400
        if len(first_name) < 2:
            return jsonify({"success": False, "message": "First name must be greater than 1 character."}), 400
        if password1 != password2:
            return jsonify({"success": False, "message": "Passwords do not match."}), 400
        if len(password1) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters."}), 400

        new_user = User(
            email=email,
            first_name=first_name,
            password=generate_password_hash(password1, method="scrypt"),
        )

        db.session.add(new_user)
        db.session.commit()

        new_user.populate_default_meals_from_json()
        login_user(new_user, remember=True)

        return jsonify({"success": True, "redirect": url_for("home.index")})

    return render_template("sign_up.html", user=current_user)
