from App.models import Workouts
from App.database import db
from App.models.workouts import Workouts

def get_all_workouts():
    return Workouts.query.all()

def get_all_workouts_json():
    workoutList = Workouts.query.all()
    if not workoutList:
        return []
    workoutList = [workout.get_json() for workout in workoutList]
    return workoutList

    #def create_workout(workoutName,description,workoutType,equipment,bodyPart,level):
        #new_workout = Workouts(workoutName=workoutName, description=description, workoutType=workoutType, equipment=equipment, bodypart=bodyPart, level=level) 
        #db.session.add(new_workout) 
        #db.session.commit() 
        #return new_workout

def get_workout_id(workout_id):
    return Workouts.query.get(workout_id)

def get_all_workouts_json():
    return Workouts.query.all()

def get_workout_difficulty(difficulty):
    return Workouts.query.filter_by(Level=difficulty).all()

def get_workout_equipment(equipment):
    return Workouts.query.filter_by(equipment=equipment).all()

def get_workout_body_part(body_part):
    return Workouts.query.filter_by(bodypart=body_part).all()

def get_workout_type(workout_type):
    return Workouts.query.filter_by(workoutType=workout_type).all()

def search_workouts(word):
    return Workouts.query.filter(Workouts.workoutName.ilike(f'%{word}%') | Workouts.description.ilike(f'%{word}%')).all()