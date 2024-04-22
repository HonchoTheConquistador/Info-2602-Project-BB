from App.database import db

class Routines(db.Model):
    routineId = db.Column(db.Integer, primary_key=True)
    routineName = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.Float, nullable=False)
    dateCreated = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50),nullable=False)
    __mapper_args__ = {
      'polymorphic_identity': 'routines',
      'polymorphic_on': type
    }

    def __init__(self,routineName,difficulty,dateCreated):
      self.routineName = routineName
      self.difficulty = difficulty
      self.dateCreated = dateCreated

    def get_json(self):
      return {
        "routineId" : self.routineId,
        "routineName" : self.routineName,
        "difficulty" : self.difficulty,
        "dateCreated" : self.dateCreated
      }

class CustomRoutine(Routines):
  __tablename__ = 'custom_routines'
  userId = db.Column(db.Integer)
  __mapper_args__ = {
    'polymorphic_identity': 'customRoutine',
  }

  def __init__(self, userID, name, difficulty, dateCreated):
    super().__init__(name,difficulty,dateCreated)
    self.userId = userID

  def get_json(self):
      return {
        "routineId" : self.routineId,
        "userId" : self.userId,
        "routineName" : self.routineName,
        "difficulty" : self.difficulty,
        "dateCreated" : self.dateCreated
      }
