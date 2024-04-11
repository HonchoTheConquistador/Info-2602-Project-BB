from App.database import db


class Workouts(db.Model):
    workoutID = db.Column(db.Integer, nullable=False,primary_key=True)
    workoutName = db.Column(db.String(50),nullable = False)
    description = db.Column(db.String, nullable=False)
    workoutType = db.Column(db.String(30),nullable = False)
    equipment = db.Column(db.String(30), nullable = False)
    bodypart = db.Column(db.String(20),nullable = False)
    Level = db.Column(db.Integer,nullable = False)
    
    def __init__(self,workoutName,description,workoutType,equipment,bodyPart,Level):
        self.workoutName = workoutName
        self.description = description
        self.workoutType = workoutType
        self.equipment = equipment
        self.bodypart = bodyPart
        self.Level = Level

    def get_json(self):
        return{
            "workoutName" : self.workoutName,
            "description" : self.description,
            "workoutType" : self.workoutType,
            "equipment" : self.equipment,
            "bodypart" : self.bodypart,
            "level" : self.level

        }