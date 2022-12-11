from app import db
from flask_login import UserMixin
import re

# many to many table
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'))
)

# Model for courswork
class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingrediants = db.Column(db.String(500), nullable=False)
    instructions = db.Column(db.String(2000), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f'<RecipeModel "{self.name}">'

    def __eq__(self, item):
        if isinstance(item, RecipeModel):
            return self.id == item.id

    # initialise variables
    def __init__(self, name, ingrediants, instructions, imageUrl, ownerID):
        self.name = name
        self.ingrediants = ingrediants
        self.instructions = instructions
        self.owner_id = ownerID

        # set deffault value if imageURL is empty
        if(imageUrl == ""):
            self.image_url = "https://img.icons8.com/fluency/512/cat-profile.png"
        else:
            self.image_url = imageUrl

    def GetInstructions(self, charCount):
        if(charCount == -1):
            return self.instructions.replace('\n', '<br>')

        reduced = self.instructions[0 : charCount]
        reduced += "..."
        return reduced.replace('\n', '<br>')

    def GetIngrediants(self):
        # Initialize an empty list to store the substrings
        substrings = []

        # Use a regular expression to find all instances of { and } in the string
        matches = re.findall(r'{([^}]*)}', self.ingrediants)

        # Loop through the matches and add each substring to the list
        for match in matches:
            # Split the substring on the | symbol
            split_substring = match.split("|")

            # Add the split substring to the list
            substrings.append(split_substring)

        # Return the list of substrings
        return substrings

# Model for courswork
class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    recipes = db.relationship('RecipeModel', backref='owner')
    favorites = db.relationship('RecipeModel', secondary=favorites, backref='followers')

    def __repr__(self):
        return f'<UserModel "{self.username}">' 

    # initialise variables
    def __init__(self, username, password, imageUrl):
        self.username = username
        self.password = password

        # set deffault value if imageURL is empty
        if(imageUrl == ""):
            self.image_url = "https://img.icons8.com/fluency/512/cat-profile.png"
        else:
            self.image_url = imageUrl