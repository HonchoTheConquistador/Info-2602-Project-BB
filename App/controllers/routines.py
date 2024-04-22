from App.models import CustomRoutine
from App.database import db
from datetime import date

#finds a specified routine by name
def get_custom_routine_by_name(name):
    return CustomRoutine.query.filter_by(routineName=name).first()


def find_custom_routine_by_id(routineId):
    routine = CustomRoutine.query.filter_by(routineId=routineId).first()
    if routine:
        return routine
    return None 

#finds a specified routine by name
def get_custom_routine_for_user(name,userID):
    return CustomRoutine.query.filter_by(routineName=name,userId=userID).first()

#gets all routines for a user
def get_all_custom_routines(userID):
    routines = CustomRoutine.query.filter_by(userId=userID).all()
    return routines

def get_all_custom_routines_json(userID):
    routines = CustomRoutine.query.filter_by(userId=userID).all()
    if not routines:
        return []
    routine_list = [routine.get_json() for routine in routines]
    return routine_list




def add_custom_routine(userID,routineName): # Adds a custom routine
    today = date.today()
    dateToday = today.strftime("%d/%m/%Y")
    try:
        customRoutine = CustomRoutine(userID, routineName, 0, dateToday) #difficulty is 0 as routine starts out empty
        db.session.add(customRoutine)
        db.session.commit()
    except:
        db.session.rollback()
        return "Error adding custom routine"
    
    return customRoutine

def delete_custom_routine(routineID): # Deletes a custom routine
    routine = CustomRoutine.query.filter_by(routineId = routineID).first()
    if routine:
        db.session.delete(routine)
        db.session.commit()
    return
    

def edit_custom_routine(routineID,name): # Edits the name of a custom routine
    routine = CustomRoutine.query.filter_by(routineId = routineID).first()
    if routine:
        routine.routineName = name
        db.session.add(routine)
        db.session.commit()
    return



