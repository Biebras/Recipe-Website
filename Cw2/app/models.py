from app import db
from flask_login import UserMixin

# Model for courswork
class UserModel(db.Model, UserMixin):
    # primary key
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(16), nullable=False)
    Password = db.Column(db.String(16), nullable=False)
    ImageUrl = db.Column(db.String(300), nullable=False)

    # initialise variables
    def __init__(self, username, password, imageUrl):
        self.Username = username
        self.Password = password

        # set deffault value if imageURL is empty
        if(imageUrl == ""):
            self.ImageUrl = "https://img.icons8.com/fluency/512/cat-profile.png"
        else:
            self.ImageUrl = imageUrl

    def get_id(self):
           return (self.UserID)

# Model for courswork
class RecipeModel(db.Model):
    # primary key
    Name = db.Column(db.Integer, primary_key=True)
    Ingrediants = db.Column(db.String(16), nullable=False)
    Instructions = db.Column(db.String(16), nullable=False)
    ImageUrl = db.Column(db.String(300), nullable=False)

    # initialise variables
    def __init__(self, username, password, imageUrl):
        self.Username = username
        self.Password = password

        # set deffault value if imageURL is empty
        if(imageUrl == ""):
            self.ImageUrl = "https://img.icons8.com/fluency/512/cat-profile.png"
        else:
            self.ImageUrl = imageUrl

    def get_id(self):
           return (self.UserID)