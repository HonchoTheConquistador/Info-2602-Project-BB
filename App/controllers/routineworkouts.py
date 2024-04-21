from App.models import RoutineWorkouts
from App.database import db

def get_all_routine_workouts(): # gets all the routine workouts from the routine workouts table 
    routines = RoutineWorkouts.query.all()
    return routines


def add_routine_workout(routineID,workoutID): # Adds a new entry to the routine workouts table 
    routineWorkout = RoutineWorkouts(routineID,workoutID)
    if routineWorkout:
        db.session.add(routineWorkout)
        db.session.commit()
    return


def delete_routine_workout(routineID,workoutID): # Deletes an entry to the routine workouts table 
    routineWorkout = RoutineWorkouts.query.filter_by(routineId=routineID,workoutId=workoutID).first()
    if routineWorkout:
        db.session.delete(routineWorkout)
        db.session.commit()
    return 

def delete_routine_workouts(routineID): # Deletes all workouts from a routine
    routineWorkouts = RoutineWorkouts.query.filter_by(routineId=routineID).all()
    if routineWorkouts:
        for workouts in routineWorkouts:
            db.session.delete(workouts)
        db.session.commit()
    return

