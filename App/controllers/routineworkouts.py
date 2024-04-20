from App.models import RoutineWorkouts
from App.database import db

def get_all_routine_workouts():
    routines = RoutineWorkouts.query.all()
    return routines


def add_routine_workout(routineID,workoutID):
    routineWorkout = RoutineWorkouts(routineID,workoutID)
    if routine:
        db.session.add(routineWorkout)
        db.commit()
        return
    else:
        return "Error adding to routine"

def delete_routine_workout(routineID,workoutID):
    routineWorkout = RoutineWorkouts.query.filter_by(routineId=routineID,workoutId=workoutID).first()
    if routineWorkout:
        db.session.delete(routineWorkout)
        db.session.commit()
    return "Error deleting from workout"

def delete_routine_workouts(routineID): #deletes all workouts from a routine
    routineWorkouts = RoutineWorkouts.query.filter_by(routineId=routineID).all()
    if routineWorkouts:
        for workouts in routineWorkouts:
            db.session.delete(workouts)
        db.session.commit()
        return
    return "Error deleting workouts"

