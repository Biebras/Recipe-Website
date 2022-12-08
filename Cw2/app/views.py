# import necessary labraries 
from flask import render_template
from app import app

# handle index template
@app.route("/")
def index():
    return render_template("index.html", title="Home Page")

@app.route("/login")
def login():
    return render_template("login.html", title="Login Page")

@app.route("/register")
def register():
    return render_template("register.html", title="Register Page")

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response