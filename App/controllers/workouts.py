from App.models import Workouts
from App.database import db
from App.models.workouts import Workouts

def get_all_workouts():
    workout_list = Workouts.query.all()
    if not workout_list:
        return []
    return [workout.get_json() for workout in workout_list]

def get_workout_id(workout_id):
    workout = Workouts.query.get(workout_id)
    return workout

def get_workout_difficulty(difficulty):
    workouts = Workouts.query.filter_by(Level=difficulty).all()
    return [workout.get_json() for workout in workouts]

def get_workout_equipment(equipment):
    workouts = Workouts.query.filter_by(equipment=equipment).all()
    return [workout.get_json() for workout in workouts]

def get_workout_body_part(body_part):
    workouts = Workouts.query.filter_by(bodypart=body_part).all()
    return [workout.get_json() for workout in workouts]

def get_workout_type(workout_type):
    workouts = Workouts.query.filter_by(workoutType=workout_type).all()
    return [workout.get_json() for workout in workouts]

def search_workouts(word):
    workouts = Workouts.query.filter(
        Workouts.workoutName.ilike(f'%{word}%') | Workouts.description.ilike(f'%{word}%')
    ).all()
    return [workout.get_json() for workout in workouts]