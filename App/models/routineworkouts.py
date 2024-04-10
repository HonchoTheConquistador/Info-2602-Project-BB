from App.database import db

class RoutineWorkouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routineId = db.Column(db.Integer, db.ForeignKey('rotines.routineId'), nullable=False)
    workoutId = db.Column(db.Integer, db.ForeignKey('workouts.workoutID'), nullable=False)

    def __init__(self, routineId, workoutId):
        self. routineId = routineId
        self.workoutId = workoutId