from App.models import Routines, FixedRoutine, CustomRoutine
from App.database import db
from datetime import date

#finds a specified routine by name
def get_routine(name):
    return Routines.query.filter_by(routineName=name)

#gets all fixed routines 
def get_all_fixed_routines():
    routines = FixedRoutine.query.all()
    return routines

def get_all_fixed_routines_json():
    routines = FixedRoutine.query.all()
    if not routines:
        return []
    routine_list = [routine.get_json() for routine in routines]
    return routine_list

#gets all custom routines 
def get_all_custom_routines(userID):
    routines = CustomRoutine.query.filter_by(userId=userID).all()
    return routines

def get_all_custom_routines_json(userID):
    routines = CustomRoutine.query.filter_by(userId=userID).all()
    if not routines:
        return []
    routine_list = [routine.get_json() for routine in routines]
    return routine_list

def get_routine_by_difficulty(difficulty): #gets routine by difficulty for fixed routines
    return FixedRoutine.query.filter_by(difficulty=difficulty).all()

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
    
    return

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

def make_fixed_routine(): #adds a fixed routine entry
    pass
