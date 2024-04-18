from App.models import userroutines, routines
from App.database import db

def get_routine_by_user(user_id):
    user_routines = UserRoutines.query.filter_by(userID=user_id).all()

    routines_details = []
    for user_routine in user_routines:
        routine = Routines.query.get(user_routine.routineId)
        if routine:
            routines_details.append({
                'routineId': routine.routineId,
                'routineName': routine.name,
                'workouts':[workouts.get_json() for workout in routine.workouts]
            })
        return routines_details

def add_workout_to_routine(routine_id, workout_id):
    routine = Routines.query.get(routine_id)
    workout = Workouts.query.get(workout_id)
    if routine and workout:
        routine.workouts.append(workout)
        db.session.commit()
        return {"success": True, "message": "Workout added to routine successfully"}
    else:
        return{"success": True, "message": "routine or Workout not found "}

def delete_workout_from_routine(routine_id, workout_id):
    routine = Routines.query.get(routine_id)
    workout = Workouts.query.get(workout_id)
    if routine and workout in routine.workouts:
        routine.workouts.remove(workout)
        db.session.commit()
        return{"success": True, "message": "Workout removed from routine successfuly"}
    else:
        return {"success": True, "message": "Routine or Workout not found or not part of the routine"}

def add_fixed_routine(name,difficulty):
    new_routine = Routines(name=name, difficulty=difficulty)
    db.session.add(new_routine)
    db.session.commit()
    return {"success": True, "message": "Fixed routine added successfully"}


def delete_fixed_routine(routine_id):
    routine = Routines.query.get(routine_id)
    if routine:
        db.session.delete(routine)
        db.session.commit()
        return {"success": True, "message": "Fixed routine deleted successfully"}
    else:
        return {"success": False, "message": "Routine not found"}



