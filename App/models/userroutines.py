from App.database import db

class UserRoutines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    routineId = db.Column(db.Integer, db.ForeignKey('routines.routineId'),nullable=False)
    
    def __init__(self, userId,routineId):
        self.userID = userId
        self.routineId = routineId
    
    def get_json():
        return {
            "userId" : self.userID,
            "routineId" : self.routineID
        }