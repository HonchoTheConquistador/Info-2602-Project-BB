from App.database import db

class Routines(db.Model):
    routineId = db.Column(db.Integer, primary_key=True)
    routineName = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.Float, nullable=False)
    dateCreated = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
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

#   todos = db.relationship(
#       'Todo', backref='user',
#       lazy=True)  # sets up a relationship to todos which references User
    __mapper_args__ = {
      'polymorphic_identity': 'customRoutine',
    }

class FixedRoutine(Routines):
  __tablename__ = 'fixed_routines'
  routineType = db.Column(db.String(120))
  __mapper_args__ = {
      'polymorphic_identity': 'fixedRoutine',
  }
  def __init__(self, routineType, name, difficulty, dateCreated):
    super().__init__(name,difficulty,dateCreated)
    self.routineType = routineType

  def get_json(self):
      return {
        "routineId" : self.routineId,
        "routineType": self.routineType,
        "routineName" : self.routineName,
        "difficulty" : self.difficulty,
        "dateCreated" : self.dateCreated
      }