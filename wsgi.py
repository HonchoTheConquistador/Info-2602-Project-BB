import click, pytest, sys
import csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, get_workout_difficulty, get_all_workouts, get_workout_equipment, get_workout_body_part, get_workout_type, search_workouts, get_workout_id )
from App.controllers import (get_all_fixed_routines, get_user_routines, add_entry_routines, delete_entry_routines)
from App.controllers import (get_all_routine_workouts, add_routine_workout, delete_routine_workout, delete_routine_workouts,make_fixed_routine,find_fixed_routine)
from App.models.workouts import Workouts
from App.models.routines import Routines, FixedRoutine
from App.models.routineworkouts import RoutineWorkouts

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    levels = ["Beginner", "Intermediate", "Expert"]
    with open('megaGymDataset.csv', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            levelsNum = levels.index(row["Level"])
            workout = Workouts(workoutName=row["Title"],description=row["Desc"],workoutType=row["Type"],equipment=row["Equipment"],bodyPart=row["BodyPart"],Level=levelsNum+1)
            db.session.add(workout)
    db.session.commit()
    with open('fixedRoutines.csv', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            routineDifficulty = 0.0 #keeps track of the difficulty of the routine based on exercises       
            name = row["Name"]
            routineType = row["RoutineType"]
            dateCreated = row["DateCreated"]
            workoutslist = row["Workouts"].split(",")
            make_fixed_routine(routineType,name,routineDifficulty,dateCreated)
            routine = find_fixed_routine(name) 
            # not sure if i have to commit it to the db first, will test 
            if routine:
                for i in workoutslist:
                    workout = Workouts.query.filter_by(workoutID =int(i)).first()
                    routineDifficulty = routineDifficulty + workout.Level
                    # add routine workout stuff here 
                    routineWorkout = RoutineWorkouts(routine.routineId,workout.workoutID)
                    db.session.add(routineWorkout)
                routineDifficulty = routineDifficulty/len(workoutslist)
                routine.difficulty = round(routineDifficulty)
                db.session.add(routine)

    db.session.commit()
    create_user('bob', 'bobpass',1)
    #Add test data here using controllers 
    print('database intialized')

#here///////////////////////////////////
workout_cli = AppGroup('workout', help='Workout management commands')

@workout_cli.command("add", help="Add a workout to a routine")
@click.argument("workout_id", type=int)
@click.argument("routine_id", type=int)
@click.argument("user_id", type=int)
def add_workout_user_command(workout_id, routine_id, user_id):
    add_entry_routines(user_id, routine_id)
    print(f"Workout {workout_id} added to routine {routine_id}")

@workout_cli.command("delete", help="Delete a workout from a routine")
@click.argument("workout_id", type=int)
@click.argument("routine_id", type=int)
@click.argument("user_id", type=int)
def delete_workout_user_command(workout_id, routine_id, user_id):
    delete_entry_routines(user_id, routine_id)
    print(f"Workout {workout_id} deleted from routine {routine_id}")

@app.cli.command("get_fixed_routines", help="Get fixed routines based on user's selected difficulty")
@click.argument("user_id", type=int)
def get_fixed_routines_user_command(user_id):
    fixed_routines = get_routine_by_difficulty(user_id)
    for routine in fixed_routines:
        print(routine.get_json())

app.cli.add_command(workout_cli)


#till here////////////////////////////
'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password,workoutLevel=1):
    create_user(username, password,workoutLevel)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''
########################################## workout.py
workouts_cli = AppGroup('workouts', help='Workout object commands')

@workouts_cli.command("get_id", help="Get workout by ID")
@click.argument("id", type=int)
def get_workout_id_command(id):
    workout = get_workout_id(id)
    if workout:
        print(workout.get_json())
    else:
        print("Workout not found")

@workouts_cli.command("get_all", help="Get all workouts")
def get_all_workouts_command():
    workouts = get_all_workouts()
    for workout in workouts:
        print(workout)

@workouts_cli.command("get_difficulty", help="Get workouts by difficulty")
@click.argument("difficulty")
def get_workouts_difficulty_command(difficulty):

    workouts = get_workout_difficulty(difficulty)
    print(workouts)

@workouts_cli.command("get_equipment", help="Get workouts by equipment")
@click.argument("equipment")
def get_workouts_equipment_command(equipment):
    workouts = get_workout_equipment(equipment)
    print(workouts)

@workouts_cli.command("get_body_part", help="Get workouts by body part")
@click.argument("body_part")
def get_workouts_body_part_command(body_part):
    workouts = get_workout_body_part(body_part)
    if workouts:
        print(workouts)
    else:
        print("No workouts found for the specified body part")

@workouts_cli.command("get_type", help="Get workouts by type")
@click.argument("workout_type")
def get_workouts_type_command(workout_type):
    workouts = get_workout_type(workout_type)
    if workouts:
        print(workouts)
    else:
        print("No workouts found for the specified type")

@workouts_cli.command("search", help="Search workouts by keyword")
@click.argument("word")
def search_workouts_command(word):
    workouts = search_workouts(word)
    if workouts:
        print(workouts)
    else:
        print("No workouts found matching the search criteria")

app.cli.add_command(workouts_cli)
##########################################

##########################################
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
##########################################

routines = AppGroup('routines' , help='Tests routine commands')

@routines.command("get_all", help="Shows all Routines")
def show_all_routines():
    routines = get_all_fixed_routines()
    for routine in routines:
        print(routine.get_json())


app.cli.add_command(routines)

######################################### userroutine.py
userroutine_tests = AppGroup('userroutine_tests', help='Testing commands for user routine controllers')

@userroutine_tests.command("get_user_routines", help="Run tests for getting user routines")
def get_user_routines_command():
    sys.exit(pytest.main(["-k", "TestGetUserRoutines"]))

@userroutine_tests.command("add_entry", help="Run tests for adding entry to user routines")
def add_entry_command():
    sys.exit(pytest.main(["-k", "TestAddEntryRoutines"]))

@userroutine_tests.command("delete_entry", help="Run tests for deleting entry from user routines")
def delete_entry_command():
    sys.exit(pytest.main(["-k", "TestDeleteEntryRoutines"]))

app.cli.add_command(userroutine_tests)
########################################## routineworkouts.py
routineworkouts_cli = AppGroup('routineworkouts', help='Routine workouts management commands')

@routineworkouts_cli.command("get_all", help="Get all routine workouts")
def get_all_routine_workouts_command():
    routine_workouts = get_all_routine_workouts()
    for routine_workout in routine_workouts:
        print(routine_workout)

@routineworkouts_cli.command("add", help="Add a workout to a routine")
@click.argument("routine_id", type=int)
@click.argument("workout_id", type=int)
def add_routine_workout_command(routine_id, workout_id):
    add_routine_workout(routine_id, workout_id)
    print(f"Workout {workout_id} added to routine {routine_id}")

@routineworkouts_cli.command("delete", help="Delete a workout from a routine")
@click.argument("routine_id", type=int)
@click.argument("workout_id", type=int)
def delete_routine_workout_command(routine_id, workout_id):
    delete_routine_workout(routine_id, workout_id)
    print(f"Workout {workout_id} deleted from routine {routine_id}")

@routineworkouts_cli.command("delete_all", help="Delete all workouts from a routine")
@click.argument("routine_id", type=int)
def delete_all_routine_workouts_command(routine_id):
    delete_routine_workouts(routine_id)
    print(f"All workouts deleted from routine {routine_id}")

app.cli.add_command(routineworkouts_cli)