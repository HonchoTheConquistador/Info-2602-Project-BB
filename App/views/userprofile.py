from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from.index import index_views

from App.controllers import (
    jwt_required,
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_fixed_routines,
    get_all_custom_routines,
    add_custom_routine,
    delete_custom_routine,
    get_user_routines,
    edit_custom_routine,
    make_fixed_routine,
    find_fixed_routine,
    add_entry_routines,
    get_routine_for_user
)

userprofile_views = Blueprint('userprofile_views', __name__, template_folder='../templates')

# @userprofile_views.route('/userprofile', methods=['GET'])
# @jwt_required() # Requires user to be logged in to view the profile
# def view_userprofile():
#     userId = jwt_current_user.id
#     customRoutines = get_all_custom_routines(userId)
#     userFixedRoutines = []
#     userR = get_user_routines(userId) 
#     userFixedRoutines = []
#     return render_template('userprofile.html',user=jwt_current_user,fixedRoutines=userFixedRoutines,customRoutines=customRoutines)  

@userprofile_views.route('/userprofile', methods=['GET'])
@jwt_required() # Requires user to be logged in to view the profile
def view_userprofile():
    user_id = jwt_current_user.id
    custom_routines = get_all_custom_routines(user_id)
    fixed_routines = get_all_fixed_routines()
    user_routines = get_user_routines(user_id)
    return render_template('userprofile.html',user=jwt_current_user,custom_routines=custom_routines,fixed_routines=fixed_routines,user_routines=user_routines)

@userprofile_views.route('/edit_custom_routine/<int:routine_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_custom_routine_route(routine_id):
    if request.method == 'POST':
        routine_name = request.form['routine_name']
        edit_custom_routine(routine_id, routine_name)
        flash(f"Custom routine {routine_name} updated!")
        return redirect(url_for('userprofile_views.view_userprofile'))
    else:
        routine = get_routine_for_user(jwt_current_user.id, routine_id)
        if routine:
            return render_template('edit_custom_routine.html', routine=routine)
        else:
            flash("Custom routine not found!")
            return redirect(url_for('userprofile_views.view_userprofile'))

@userprofile_views.route('/delete_custom_routine/<int:routine_id>', methods=['POST'])
@jwt_required()
def delete_custom_routine_route(routine_id):
    delete_custom_routine(routine_id)
    flash("Custom routine deleted!")
    return redirect(url_for('userprofile_views.view_userprofile'))

@userprofile_views.route('/create_custom_routine', methods=['POST'])
@jwt_required()
def create_custom_routine():
    routine_name = request.form['routine_name']
    add_custom_routine(jwt_current_user.id, routine_name)
    flash(f"Custom routine {routine_name} created!")
    return redirect(url_for('userprofile_views.view_userprofile'))
    
# @userprofile_views.route('/addCustomRoutine', methods=["POST"])
# # @jwt_required()
# def add_custom_routine_userprofile():
#     userId = jwt_current_user.id
    
#     add_custom_routine(userId,"test")
#     routine = get_routine_for_user("test",userId)
#     add_entry_routines(userId,routine.routineId)
#     redirect(url_for('userprofile'))

# @homepage_views.route('/custom_routines', methods=['GET'])
# @jwt_required()
# def get_custom_routines():
#     user_id = jwt_current_user.id
#     custom_routines = get_all_custom_routines(user_id)
#     return render_template('custom_routines.html', custom_routines)