from App.models import userroutines
from App.database import db

def get_user_routines():
    return RoutineWorkouts.query.all()

