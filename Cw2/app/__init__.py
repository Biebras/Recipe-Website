from flask import Flask
from flask import render_template;
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging import FileHandler, WARNING
import logging

# set necessary variables, to easily access them later
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db,render_as_batch=True)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

logging.basicConfig(level=logging.DEBUG)
file_handler = FileHandler("errorlog.txt")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

from app import views
from app import models