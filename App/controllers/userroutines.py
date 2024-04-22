from App.models import UserRoutines
from App.database import db
    
def get_user_routines(user_id): # gets all routines associated with the user
    user_routines = UserRoutines.query.filter_by(userID=user_id).all()
    if user_routines:
        return user_routines
    return None

def get_user_routines_json(user_id): # gets all routines associated with the user
    user_routines = UserRoutines.query.filter_by(userID=user_id).all()
    if user_routines:
        return [user_routine.get_json( ) for user_routine in user_routines]
    return None
    
def add_user_routines(user_id, routine_id):
    try:
        user_routine = UserRoutines(userID=user_id, routineId=routine_id)
        db.session.add(user_routine)
        db.session.commit()
        return 
    except Exception as e:
        db.session.rollback()
        return 

def delete_user_routines(user_id, routine_id):
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
