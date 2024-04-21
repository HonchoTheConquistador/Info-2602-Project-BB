from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import (
    create_user,
    get_all_fixed_routines,
    get_all_custom_routines,
    add_custom_routine,
    delete_custom_routine,
    get_user_routines,
    edit_custom_routine,
    add_entry_routines,
    get_routine_for_user,
    find_fixed_routine_by_id,
    get_all_custom_routines_json,
    get_user_routines_json,
    get_fixed_routine_by_id,
    get_workouts_by_routine,
    get_workout_id
)

userprofile_views = Blueprint('userprofile_views', __name__, template_folder='../templates')

@userprofile_views.route('/userprofile', methods=['GET'])
@jwt_required()
def view_userprofile():
    user_id = jwt_current_user.id
    custom_routines = get_all_custom_routines(user_id)
    
    user_routines = get_user_routines(user_id)
    fixed_routines = get_all_fixed_routines()
    user_fixed_routines = []
    if user_routines:
        for j in user_routines:
            obj = find_fixed_routine_by_id(j.routineId)
            if obj:
                user_fixed_routines.append(obj)
    
    return render_template('userprofile.html',user=jwt_current_user,customRoutines=custom_routines,fixedRoutines=user_fixed_routines,user_routines=user_routines)

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

@userprofile_views.route('/add_fixed_routine', methods=['POST'])
@jwt_required() 
def add_fixed_routine_to_user():
    user_id = jwt_current_user.id
    routine_id = request.form['routine_id']
    add_entry_routines(user_id, routine_id)
    remove_fixed_routine(routine_id)
    return redirect(url_for('userprofile_views.view_userprofile'))

@userprofile_views.route('/api/customRoutine', methods=['GET'])
def custRoutine_endpt():
    user_id = jwt_current_user.id
    routines = get_all_custom_routines_json(user_id)
    return jsonify(routines)

@userprofile_views.route('/api/addCustomRoutine', methods=["POST"])
def add_custom_routine_userprofile():
    user_id = jwt_current_user.id
    request_data = request.json
    routine_name = request_data.get('routine_name', None)
    if routine_name is None:
        return jsonify({'error': 'Routine name is required'}),
    add_custom_routine(user_id, routine_name)
    routine = get_routine_for_user(routine_name, user_id)
    add_entry_routines(user_id, routine.routineId)
    return jsonify({'message': f"User {user_id} has created a new custom routine with name '{routine_name}'"})

@userprofile_views.route('/api/getUserRoutines', methods=["GET"])
@jwt_required()
def get_user_routines_userprofile():
    user_id = jwt_current_user.id
    routines = get_user_routines_json(user_id)
    return jsonify(routines)

@userprofile_views.route('/create_custom_routine', methods=['GET', 'POST'])
@jwt_required()
def create_custom_routine_p2():
    if request.method == 'GET':
        # Display the form to the user
        return render_template('custom_details.html')

    if request.method == 'POST':
        # Process the form data to create a new routine
        routine_name = request.form.get('routineName')
        routine_description = request.form.get('routineDescription')
        routine_type = request.form.get('routineType')

        if not routine_name:
            flash('Routine name is required!', 'error')
            return redirect(url_for('userprofile_views.create_custom_routine'))

        # Create a new routine instance
        new_routine = CustomRoutine(name=routine_name,description=routine_description,type=routine_type,user_id=current_user.id) # Assuming you're using current_user to get the logged-in user ID
        db.session.add(new_routine)
        try:
            db.session.commit()
            flash('New routine created successfully!', 'success')
            return redirect(url_for('userprofile_views.view_userprofile'))
        except:
            db.session.rollback()
            flash('Failed to create a new routine.', 'error')
            return redirect(url_for('userprofile_views.create_custom_routine'))

# Assuming you have a route to show the form
#@userprofile_views.route('/new_custom_routine', methods=['GET'])
#@jwt_required()
#def new_custom_routine_form():
#    return render_template('create_custom_routine.html')




# @userprofile_views.route('/userprofile', methods=['GET'])
# @jwt_required() # Requires user to be logged in to view the profile
# def view_userprofile():
#     userId = jwt_current_user.id
#     customRoutines = get_all_custom_routines(userId)
#     userFixedRoutines = []
#     userR = get_user_routines(userId) 
#     userFixedRoutines = []
#     return render_template('userprofile.html',user=jwt_current_user,fixedRoutines=userFixedRoutines,customRoutines=customRoutines)  

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

# @userprofile_views.route('/api/addCustomRoutine', methods=["GET"])
# def add_custom_routine_userprofile():
#     userId = 1
#     name = "test"
#     add_custom_routine(userId,name)
#     routine = get_routine_for_user(name,userId)
#     add_entry_routines(userId, routine.routineId)
#     return jsonify({'message':f"user {userId} has created a new custom routine"})