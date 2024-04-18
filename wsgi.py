import click, pytest, sys
import csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users)
from App.models.workouts import Workouts


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
    with open('megaGymDataset.csv', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            routineDifficulty = 0.0 #keeps track of the difficulty of the routine based on exercises       

            routine = FixedRoutine()
            db.session.add(routine)

    db.session.commit()
    create_user('bob', 'bobpass',1)
    print('database intialized')


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
##########################################
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
    print(workouts)

@workouts_cli.command("get_difficulty", help="Get workouts by difficulty")
@click.argument("difficulty")
def get_workouts_difficulty_command(difficulty):
    workouts = get_workouts_difficulty(difficulty)
    print(workouts)

@workouts_cli.command("get_equipment", help="Get workouts by equipment")
@click.argument("equipment")
def get_workouts_equipment_command(equipment):
    workouts = get_workouts_equipment(equipment)
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
