from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, create_access_token
from sqlalchemy.exc import IntegrityError
from App.models import User
from App.controllers import create_user, login

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''
@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template("signup.html")

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    try:
        username = data['username']
        password = data['password']
        workoutLevel = data['workoutLevel']
        
        user, error_message = create_user(username, password, workoutLevel)
        
        if user:
            token = create_access_token(identity=user.id)
            response = redirect(url_for('homepage_views.homepage'))
            set_access_cookies(response, token)
            flash('Account created successfully', 'success')
            return response, 201
        else:
            flash('Failed to create account: ' + error_message, 'error')
            return redirect(url_for('auth_views.signup_page')), 400
    except IntegrityError:
        flash('Username already exists', 'error')
        return redirect(url_for('auth_views.signup_page')), 400
    except KeyError:
        flash('Invalid request data', 'error')
        return redirect(url_for('auth_views.signup_page')), 400

@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('layout.html', title='Login') 

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Bad username or password given', 'error')  # Add 'error' category for flash message
        return redirect(url_for('auth_views.login'))  
    else:
        flash('Login Successful', 'success')  # Add 'success' category for flash message
        response = redirect(url_for('homepage_views.homepage'))  
        set_access_cookies(response, token)
        return response
    
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.login_page'))  
    unset_jwt_cookies(response)  
    flash("Logged Out!", 'success')

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response


@auth_views.route('/api/signup', methods=['POST'])
def signup_page_endpoint():
    data = request.json
    username = data['username']
    password = data['password']
    workoutLevel = data['workoutLevel']
    newuser = create_user(username,password,workoutLevel)
    response = None
    if newuser:
        
        return jsonify({"message": f"{newuser.username} was signed up"})
    else:
        return jsonify({"message": f"Failure in was signed up"})
    