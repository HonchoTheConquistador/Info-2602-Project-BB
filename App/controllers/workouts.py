from App.models import Workouts
from App.database import db

def get_all_workouts():
    return Workouts.query.all()

def get_all_workouts_json():
    workoutList = Workouts.query.all()
    if not workoutList:
        return []
    workoutList = [workout.get_json() for workout in workoutList]
    return workoutList


