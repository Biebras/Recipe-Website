from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

# create db
db.create_all()