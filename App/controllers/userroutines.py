from App.models import userroutines, routines
from App.database import db

def get_user_fixedRoutines():
    user_fixedRoutines = FixedRoutines.query.filter_by(userID=user_id).all()
    user_fixedRoutines_details = []
    for user_fixedRoutine in user_fixedRoutines:
        fixedRoutine = FixedRoutine.query.get(user_fixedRoutine.fixedRoutineId)
        if fixedRoutine:
            fixedroutines_details.append({
        "routineId" : routineId,
        "routineType": routineType,
        "routineName" : routineName,
        "difficulty" : difficulty,
        "dateCreated" : dateCreate,
            })
    return fixedroutines_details

                          

def get_user_routines(user_id):
    user_routines = UserRoutines.query.filter_by(userID=user_id).all()
    routines_details = []
    for user_routine in user_routines:
        routine = Routine.query.get(user_routine.routineId)
        if routine:
            routines_details.append({
                'routineId': routine.id,
                'routineName': routine.name,
            })
    return routines_details
    
def add_workout_routine(user_id,routine_id):
    routine = Routine.query.get(routine_id)
    if not routine:
        return {"success": False, "message": "Routine not found"}
        workout = Workouts.query.get(workout_id)
    if not workout:
        return {"success": False, "message": "Workout not found"}
    if workout in routine.workouts:
        return {"success": False, "message": "Workout already exists in the routine"}
    routine.workouts.append(workout)
    db.session.commit()
    return {"success": True, "message": "Workout added to routine successfully"}

def delete_workout_from_routine(routine_id):
    routine = Routine.query.get(routine_id)
    if not routine:
        return {"success": False, "message": "Routine not found"}
    workout = Workouts.query.get(workout_id)
    if not workout:
        return {"success": False, "message": "Workout not found"}
    if workout not in routine.workouts:
        return {"success": False, "message": "Workout is not part of the routine"}
    routine.workouts.remove(workout)
    db.session.commit()
    return {"success": True, "message": "Workout removed from routine successfully"}



