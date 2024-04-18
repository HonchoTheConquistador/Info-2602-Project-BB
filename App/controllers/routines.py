from App.models import Routines
from App.database import db

#finds a specified routine by name
def get_routine(name):
    return Routines.query.filter_by(routineName=name)

#gets all routines 
def get_all_routines():
    routine = FixedRoutine.query.all()
    return Routines.query.all()

def get_all_routines_json():
    routines = FixedRoutine.query.all()
    if not routines:
        return []
    routine_list = [routine.get_json() for routine in routines]
    return routine_list

def get_routine_by_difficulty(difficulty):
    return FixedRoutine.query.filter_by(difficulty=difficulty).all()



