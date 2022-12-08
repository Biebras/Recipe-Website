from app import db

# Model for courswork
class CwModel(db.Model):
    # primary key
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100))
    Password = db.Column(db.String(20))
    ImageUrl = db.Column(db.String(100))

    # initialise variables
    def __init__(self, username, password, imageUrl):
        self.Username = username
        self.Password = password
        self.ImageUrl = imageUrl