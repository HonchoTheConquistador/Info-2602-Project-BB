from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_fixed_routines,
    get_all_custom_routines,
    add_custom_routine,
    delete_custom_routine,
    edit_custom_routine,
    make_fixed_routine,
    find_fixed_routine
)

homepage_views = Blueprint('homepage_views', __name__, template_folder='../templates')

@homepage_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users)

@homepage_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@homepage_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@homepage_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@homepage_views.route('/redirect_to_userprofile', methods=['GET'])
@jwt_required()
def redirect_to_userprofile():
    return redirect(url_for('userprofile_views.view_userprofile'))