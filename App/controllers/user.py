from App.models import User
from App.database import db

def create_user(username, password,workoutLevel):
    newuser = User(username=username, password=password,workoutLevel=workoutLevel)
    try:
        db.session.add(newuser)
        db.session.commit()
    except Exception:  # attempted to insert a duplicate user
        db.session.rollback()
        flash("username or email already exists")  # error message
        return None
    return newuser


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    