from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({'success': True, 'redirect': url_for('home.index')})
        else:
            return jsonify({'success': False, 'message': 'Incorrect email or password, please try again.'})
    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'success': False, 'message': 'Email already exists.'})
        elif len(email) < 6:
            return jsonify({'success': False, 'message': 'Email must be greater than 6 characters.'})
        elif len(first_name) < 2:
            return jsonify({'success': False, 'message': 'First name must be greater than 1 character.'})
        elif password1 != password2:
            return jsonify({'success': False, 'message': 'Passwords don\'t match.'})
        elif len(password1) < 8:
            return jsonify({'success': False, 'message': 'Password must be at least 8 characters.'})
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='scrypt')
            )
            db.session.add(new_user)
            db.session.commit()
            new_user.populate_default_meals_from_json()
            login_user(new_user, remember=True)
            return jsonify({'success': True, 'redirect': url_for('home.index')})
    return render_template("sign_up.html", user=current_user)