from flask import Flask
from flask import render_template;

# set necessary variables, to easily access them later
app = Flask(__name__)

from app import views