# import necessary labraries 
from flask import render_template, request, redirect
from app import app, db, login_manager
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm
from .models import UserModel

# handle index template
@app.route("/")
def index():
    return render_template("index.html", title="Home Page")

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(Username=form.Username.data).first
        print(form.Username.data)

        if(user):
            if(user.Password != form.Password.data):
                alert("Wrong password")
            else:
                login_user(user)
                return redirect("/")

    return render_template("login.html", title="Login Page", form = form)

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
def load_user(user_id):
    return UserModel.query.get(int(user_id))