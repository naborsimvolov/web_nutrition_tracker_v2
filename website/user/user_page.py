from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..models import update_user_goals

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/profile')
@login_required
def profile():
    return render_template('userprofile.html', user=current_user)

@user_profile.route('/save-goals', methods=['POST'])
@login_required
def save_goals():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    try:
        # user goals in database update
        update_user_goals(
            user=current_user,
            calories_goal=data.get('calories'),
            carbs_goal=data.get('carbs'),
            proteins_goal=data.get('proteins'),
            fats_goal=data.get('fats')
        )
        return jsonify({'success': 'Goals saved successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500