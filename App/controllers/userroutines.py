from App.models import userroutines, routines
from App.database import db

def get_all_routines():
    routines_list = Routines.query.all()
    if not routines_list:
        return []
    return [routine.get_json() for routine in routines_list]

def get_routine_id(routine_id):
    routine = Routines.query.get(routine_id)
    return routine

def get_user_id(user_id):
    user = Users.query.get(user_id)
    return user

def
    
def add_workout_routine(routine_id, workout_id):
    routine = Routine.query.get(routine_id)
    if not routine:
        return {"success": False, "message": "Routine not found"}
        db.session.commit()
        return{"success": True, "message": "Workout added to routine successfully"}

def delete_workout_routine(routine_id, workout_id):
    routine = Routine.query.get(routine_id)
    if not routine:
        return {"success": False, "message": "Routine not found"}
    db.session.commit()
    return {"success": True, "message": "Workout removed from routine successfully"}



