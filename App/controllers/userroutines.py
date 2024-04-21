from App.models import UserRoutines
from App.database import db

def get_fixed_routines():
    fixed_routines_list = FixedRoutine.query.all()
    if not fixed_routines_list:
        return []
    return [fixed_routine.get_json() for fixed_routine in fixed_routines_list] 

def get_routine_id(routine_id):
    routine = Routines.query.get(routine_id)
    return routine

def get_user_id(user_id):
    user = Users.query.get(user_id)
    return user
    
def get_user_routines(user_id): # gets all routines associated with the user, including both custom and fixed routines
    user_routines = UserRoutines.query.filter_by(userID=user_id).all()
    # routines_details = []
    # for user_routine in user_routines:
    #     routine = Routine.query.get(user_routine.routineId)
    #     if routine:
    #         routine_details = routine.get_json()
    #         routine_details["routineId"] = user_routine.id
    #         routines_details.append(routine_details)
    if user_routines:
        return user_routines
    return None
    
def add_entry_routines(user_id, routine_id):
    try:
        user_routine = UserRoutines(userId=user_id, routineId=routine_id)
        db.session.add(user_routine)
        db.session.commit()
        return {"success": True, "message": "Entry added to user routines successfully"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}

def delete_entry_routines(user_id, routine_id):
    user_routine = UserRoutines.query.filter_by(userID=user_id, routineId=routine_id).first()
    if user_routine:
        try:
            db.session.delete(user_routine)
            db.session.commit()
            return {"success": True, "message": "Entry deleted from user routines successfully"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}
    else:
        return {"success": False, "message": "Entry not found in user routines"}
