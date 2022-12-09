# import necessary labraries 
from flask import render_template, request, redirect, flash
from app import app, db, login_manager
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm, AddRecipe
from .models import UserModel

# handle index template
@app.route("/")
def index():
    return render_template("index.html", title="Home Page", user = current_user)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        user = UserModel.query.filter_by(username=form.username.data).first()

        if(user):
            if(user.password != form.password.data):
                flash("Password or username was incorrect")
            else:
                login_user(user)
                return redirect("/")
        else:
            flash("Password or username was incorrect")

    return render_template("login.html", title="Login Page", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    #Create form
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if(form.password.data != form.confirmPassword.data):
            flash("Passwords should match")

    if(request.method == 'POST' and form.validate() == False):
        flash(form.errors)

    if request.method == 'POST' and form.validate():
        newUser = UserModel(form.username.data, form.password.data, form.profileUrl.data)
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        return redirect("/")

    return render_template("register.html", title="Register Page", form = form)

@app.route("/addRecipe", methods=["POST", "GET"])
def addRecipe():
    #Create form
    form = AddRecipe(request.form)

    if(request.method == 'POST' and form.validate() == False):
        flash(form.errors)

    return render_template("addRecipe.html", title="Add Recipe Page", user = current_user, form = form)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@login_manager.user_loader
def load_user(userID):
    return UserModel.query.get(userID)