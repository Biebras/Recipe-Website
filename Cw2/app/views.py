# import necessary labraries 
from flask import render_template, request, redirect, flash
from app import app, db, login_manager
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm, RecipeForm, ProfileForm
from .models import UserModel, RecipeModel

current_recipe_id = None

# handle index template
@app.route("/")
def index():
    app.logger.info('index route request')
    mostPupularRecipe = None
    allRecipes = RecipeModel.query.all()
    
    sortedRecipies = sorted(allRecipes, key=lambda x: len(x.followers), reverse=True)

    if(len(sortedRecipies) is not 0):
        mostPupularRecipe = sortedRecipies[0]
        sortedRecipies.remove(mostPupularRecipe)

    popularRecipies = sortedRecipies[:3]
    app.logger.info('render index template')
    return render_template("index.html", title="Home Page", user = current_user, favorite = mostPupularRecipe, popularRecipies = popularRecipies)

@app.route("/login", methods=["POST", "GET"])
def login():
    app.logger.info("login route request")
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        app.logger.info("login form validate success")
        user = UserModel.query.filter_by(username=form.username.data).first()

        if(user.password != form.password.data):
            app.logger.warning("Password or username was incorrect, refresing login page")
            flash("Password or username was incorrect")
            return render_template("login.html", title="Login Page", form = form)

        if(user):
            login_user(user, remember=form.rememberMe.data)
            app.logger.info("user successfully loged in, redirecting to index")
            return redirect("/")
        else:
            app.logger.warning("User was not found, login failed")


    app.logger.info("rendering login template")
    return render_template("login.html", title="Login Page", form = form)

@app.route("/logout")
@login_required
def logout():
    app.logger.info("logout request")
    logout_user()
    app.logger.info("logout successful, redirecting to index")
    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    app.logger.info("register route request")
    #Create form
    form = RegisterForm(request.form)

    if(request.method == "POST"):
        app.logger.info("register form posted")
        if(form.password.data != form.confirmPassword.data):
            flash("Passwords should match")
            app.logger.warning("Registration failed, passwords don't match, refreshin register page")
            return render_template("register.html", title="Register Page", form = form)

    if request.method == 'POST' and form.validate():
        app.logger.info("register form validate success")

        # Check if user is already in database
        user = UserModel.query.filter_by(username=form.username.data).first()

        if user is not None:
            flash('Username already taken. Please choose a different username.')
            app.logger.warning("Registration failed, username is already taken, refreshin register page")
            return render_template("register.html", title="Register Page", form = form)

        app.logger.info("Crating new user")
        newUser = UserModel(form.username.data, form.password.data, form.profileUrl.data)
        db.session.add(newUser)
        db.session.commit()
        app.logger.info("New user commited to the database")
        login_user(newUser)
        app.logger.info("user successfully signed in, logining user and redirecting to index")
        return redirect("/")

    app.logger.info("rendering register template")
    return render_template("register.html", title="Register Page", form = form)

@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    app.logger.info("profile route request")
    form = ProfileForm(request.form)

    if request.method == 'POST':
        app.logger.info("profile form posted")

        if(form.password.data != form.confirmPassword.data):
            flash("Passwords should match")
            app.logger.warning("Profile failed, passwords don't match, refreshin profile page")
            return render_template("profile.html", title="All Recipes Page", user = current_user, form = form)
    
    if request.method == 'POST' and form.validate():
        app.logger.info("profile form validate success")

        if(current_user.password == form.password.data):
            flash("Your new password can't be your old password")
            app.logger.warning("Profile failed, new password is old password, refreshin profile page")
            return render_template("profile.html", title="All Recipes Page", user = current_user, form = form)

        if(form.password.data != ""):
            app.logger.info("changing user password")
            current_user.password = form.password.data

        current_user.image_url = form.profileUrl.data
        db.session.commit()
        app.logger.info("user changes commited to database, refreshing page to index")
        return redirect("/")

    app.logger.info("rendering profile template")
    return render_template("profile.html", title="All Recipes Page", user = current_user, form = form)

@app.route("/allRecipies", methods=["POST", "GET"])
def allRecipies():
    allRecipies = RecipeModel.query.all()
    return render_template("allRecipies.html", title="All Recipes Page", user = current_user, allRecipies = allRecipies)

@app.route("/yourRecipies", methods=["POST", "GET"])
@login_required
def yourRecipies():
    return render_template("yourRecipies.html", title="All Recipes Page", user = current_user, yourRecipies = current_user.recipes)

@app.route("/favoritesRecipies", methods=["POST", "GET"])
@login_required
def favoriteRecipies():
    return render_template("favoriteRecipies.html", title="All Recipes Page", user = current_user, favoriteRecipies = current_user.favorites)

@app.route("/addRecipe", methods=["POST", "GET"])
@login_required
def addRecipe():
    #Create form
    form = RecipeForm(request.form)

    if(request.method == 'POST' and form.validate() == False):
        print("Hmm?")
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
    recipe = get_current_recipe()
    followers_count = len(recipe.followers)
    return render_template("recipe.html", title="Recipe Page", user = current_user, current_recipe = recipe, followers_count = followers_count)

@app.route("/findRecipe/<int:id>", methods=["POST", "GET"])
def findRecipe(id):
    global current_recipe_id
    current_recipe_id = id
    return redirect("/recipe")

@app.route("/followRecipe", methods=["POST", "GET"])
@login_required
def followRecipe():
    recipe = get_current_recipe()
    current_user.favorites.append(recipe)
    db.session.commit()
    return redirect("/recipe/")

@app.route("/unfollowRecipe", methods=["POST", "GET"])
@login_required
def unfollowRecipe():
    recipe = get_current_recipe()
    current_user.favorites.remove(recipe)
    db.session.commit()
    return redirect("/recipe")

@app.route("/deleteRecipe", methods=["POST", "GET"])
@login_required
def deleteRecipe():
    recipe = get_current_recipe()

    if(recipe.owner.id != current_user.id):
        return redirect("/")

    db.session.delete(recipe)
    db.session.commit()
    return redirect("/")

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@login_manager.user_loader
def load_user(userID):
    return UserModel.query.get(userID)

def get_current_recipe():
    return RecipeModel.query.get(current_recipe_id)