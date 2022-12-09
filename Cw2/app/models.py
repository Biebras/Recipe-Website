from app import db
from flask_login import UserMixin

# Model for courswork
class RecipeModel(db.Model):
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingrediants = db.Column(db.String(500), nullable=False)
    instructions = db.Column(db.String(2000), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    # initialise variables
    def __init__(self, name, ingrediants, instructions, imageUrl, ownerID):
        self.name = name
        self.ingrediants = ingrediants
        self.instructions = instructions
        self.owner_id = ownerID

        # set deffault value if imageURL is empty
        if(image_url == ""):
            self.image_url = "https://img.icons8.com/fluency/512/cat-profile.png"
        else:
            self.image_url = imageUrl

# Model for courswork
class UserModel(db.Model, UserMixin):
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    recipes = db.relationship('RecipeModel', backref='user')

    # initialise variables
    def __init__(self, username, password, imageUrl):
        self.username = username
        self.password = password

        # set deffault value if imageURL is empty
        if(imageUrl == ""):
            self.image_url = "https://img.icons8.com/fluency/512/cat-profile.png"
        else:
            self.image_url = imageUrl