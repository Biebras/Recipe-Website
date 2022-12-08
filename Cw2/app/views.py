# import necessary labraries 
from flask import render_template, request, redirect, flash
from app import app, db, login_manager
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm
from .models import UserModel

# handle index template
@app.route("/")
def index():
    return render_template("index.html", title="Home Page", user = current_user)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        user = UserModel.query.filter_by(Username=form.Username.data).first()
        # print(load_user(1).Username)

        if(user):
            if(user.Password != form.Password.data):
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
        if(form.Password.data != form.ConfirmPassword.data):
            flash("Passwords should match")

    if request.method == 'POST' and form.validate():
        newUser = UserModel(form.Username.data, form.Password.data, form.ProfileUrl.data)
        db.session.add(newUser)
        db.session.commit()
        return redirect("/")

    return render_template("register.html", title="Register Page", form = form)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@login_manager.user_loader
def load_user(userID):
    return UserModel.query.get(userID)