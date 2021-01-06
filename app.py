import os 
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from passcheck import passcheck
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# landing page
@app.route("/")
@app.route("/get_exercises")
def get_exercises():
    exercises = mongo.db.exercises.find()
    return render_template("exercises.html", exercises=exercises)   


# register and sign up page
@app.route("/register", methods=["GET", "POST"])
def register():
    '''
    Will render register page and handle account register 
    and post user details into database or check to see if 
    user already exists.
    '''
    if request.method == "POST":
        # register form - checks if user is already in database.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists, please try another one or log in.")
            return redirect(url_for("register"))

        # posts new user details to database, hashes password.
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Success! You are now registered.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Will render log in page and create session cookie for user session.
    '''
    # log in form - checks if user is registered
    if request.method == "POST":
        username_confirmed = mongo.db.users.find_one(
        {"username": request.form.get("loginusername").lower()})
        
        if username_confirmed:
            # checks that hashed password matches user input and creates session cookie
            if check_password_hash(
                username_confirmed["password"], request.form.get("loginpassword")):
                    session["user"] = request.form.get("loginusername").lower()
                    flash("Welcome back, {}".format(request.form.get("loginusername")))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                # if password does not match
                flash("Details are incorrect, please try again")
                return redirect(url_for("login"))
        else:
            # username is not in database
            flash("Incorrect details, please try again")
            return render_template("login")

    return render_template("login.html")


# Log out functionality route
@app.route("/logout")
def logout():
    # will pop user session cookie out of memory
    flash("You have been successfully logged out!")
    session.pop("user")
    return redirect(url_for("get_exercises"))


# Profile page route
@app.route("/profile", methods=["GET", "POST"])
def profile():
    '''
    Will render profile page and create exercise form. 
    Allowing session user to add exercises to the database.
    Will also take users username from database.
    '''
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    if session["user"]:
        exercises = mongo.db.exercises.find()
        return render_template("profile.html", 
        username=username, exercises=exercises)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
