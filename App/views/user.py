from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from sqlalchemy.exc import IntegrityError
from.index import index_views
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json, 
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():  
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'], data['workoutLevel'])
    return jsonify({'message': f"user {user.username} created with id {user.id} and workout Level {user.workoutLevel}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    try:
        username = data['username']
        password = data['password']
        workoutLevel = data['workoutLevel']
    
        user = create_user(username, password, workoutLevel)
        
        if user:
            token = create_access_token(identity=user.id)
            response = redirect(url_for('homepage_views.homepage'))
            set_access_cookies(response, token)
            flash('Account created successfully', 'success')
            return response, 201
        else:
            flash('Username or email already exists', 'error')
            return redirect(url_for('auth_views.signup_page')), 400
    except IntegrityError:
        flash('Username already exists', 'error')
        return redirect(url_for('auth_views.signup_page')), 400
    except KeyError:
        flash('Invalid request data', 'error')
        return redirect(url_for('auth_views.signup_page')), 400