from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from.index import index_views

from App.controllers import (
    create_user,
    login,
    
)
from App.controllers import get_all_fixed_routines_json

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")

@auth_views.route("/signup", methods=['GET'])
def signup_page():
    return render_template("signup.html")

@auth_views.route("/signup", methods=['POST'])
def signup_action():
    response = None
    try:
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        response = redirect(url_for('homepage_views.homepage'))
        token = create_access_token(identity=user)
        set_access_cookies(response, token)
    except IntegrityError:
        flash('Username already exists')
        response = redirect(url_for('signup_page'))
    flash('Account created')
    return response



@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('layout.html', title='Login') 

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Bad username or password given'), 401
        return redirect(url_for('auth_views.login'))  
    else:
        flash('Login Successful')
        response = redirect(url_for('homepage_views.homepage'))  
        set_access_cookies(response, token)
        return response
    
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.login_page'))  
    unset_jwt_cookies(response)  
    flash("Logged Out!")
    return response
    


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
        # Handle invalid credentials
        return jsonify({"message": f"Failure in was signed up"})
    