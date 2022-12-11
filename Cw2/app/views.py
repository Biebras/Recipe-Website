# import necessary labraries 
from flask import render_template, request, redirect, flash
from app import app, db, login_manager
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm, RecipeForm
from .models import UserModel, RecipeModel
import time

current_recipe = None

# handle index template
@app.route("/")
def index():
    mostPupularRecipe = None
    allRecipes = RecipeModel.query.all()
    
    sortedRecipies = sorted(allRecipes, key=lambda x: len(x.followers), reverse=True)

    if(len(sortedRecipies) is not 0):
        mostPupularRecipe = sortedRecipies[0]
        sortedRecipies.remove(mostPupularRecipe)

    popularRecipies = sortedRecipies[:6]

    return render_template("index.html", title="Home Page", user = current_user, favorite = mostPupularRecipe, popularRecipies = popularRecipies)

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

@app.route("/allRecipies", methods=["POST", "GET"])
def allRecipies():
    allRecipies = RecipeModel.query.all()
    return render_template("allRecipies.html", title="All Recipes Page", user = current_user, allRecipies = allRecipies)

@app.route("/addRecipe", methods=["POST", "GET"])
@login_required
def addRecipe():
    #Create form
    form = RecipeForm(request.form)

    if(request.method == 'POST' and form.validate() == False):
        ingrediants = ""
        for x in form.ingrediants:
            ingrediants += "{" + x.ingrediant.data + "|" + x.quantity.data + "}"
        
        recipe = RecipeModel(form.name.data, ingrediants, form.instructions.data, form.image_url.data, current_user.id)
        db.session.add(recipe)
        db.session.commit()
        return redirect("/")

    return render_template("addRecipe.html", title="Add Recipe Page", user = current_user, form = form)

@app.route("/recipe/", methods=["POST", "GET"])
def recipe():
    return render_template("recipe.html", title="Recipe Page", user = current_user, current_recipe = current_recipe)

@app.route("/findRecipe/<int:id>", methods=["POST", "GET"])
def findRecipe(id):
    global current_recipe
    current_recipe = RecipeModel.query.get(id)
    return redirect("/recipe")

@app.route("/followRecipe", methods=["POST", "GET"])
@login_required
def followRecipe():
    current_user.favorites.append(current_recipe)
    db.session.commit()
    print(current_recipe)
    return redirect("/recipe")

@app.route("/unfollowRecipe", methods=["POST", "GET"])
@login_required
def unfollowRecipe():
    current_user.favorites.remove(current_recipe)
    db.session.commit()
    # Wait for commit end before turning recipe
    time.sleep(0.1)
    return redirect("/recipe")

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@login_manager.user_loader
def load_user(userID):
    return UserModel.query.get(userID)