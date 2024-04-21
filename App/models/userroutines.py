from App.database import db

class UserRoutines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    routineId = db.Column(db.Integer, db.ForeignKey('routines.routineId'),nullable=False)
    
    def __init__(self, userID,routineId):
        self.userID = userID
        self.routineId = routineId
    
    def get_json(self):
        return {
            "userId" : self.userID,
            "routineId" : self.routineId
        }