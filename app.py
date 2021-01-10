import os 
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
def home():
    '''
    This function loads the home landing page.
    '''
    exercises = mongo.db.exercises.find()
    
    return render_template("pages/home.html", exercises=exercises)   


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
        return render_template("pages/profile.html", username=session["user"])

    return render_template("pages/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Will render log in page and create session cookie
    for user session.
    '''
    # log in form - checks if user is registered
    if request.method == "POST":
        username_confirmed = mongo.db.users.find_one(
        {"username": request.form.get("loginusername").lower()})
        
        if username_confirmed:
            # checks that hashed password matches user input and creates session cookie
            if check_password_hash(
                username_confirmed["password"], request.form.get("loginpassword")):
                    session["user"] = request.form.get(
                        "loginusername").lower()
                    flash("Welcome back, {}".format(
                        request.form.get("loginusername")))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                # if password does not match
                flash("Incorrect details, please try again")
                return redirect(url_for("login"))
        else:
            # username is not in database
            flash("Incorrect details, please try again")
            return render_template("pages/login.html")

    return render_template("pages/login.html")


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

    if username:
        userexercises = mongo.db.exercises.find({ "user": username })
        return render_template("pages/profile.html", username=username, userexercises=list(userexercises))

    return redirect(url_for("login"))


# Log out functionality route
@app.route("/logout")
def logout():
    '''
    will pop user session cookie out of memory
    '''
    flash("You have been successfully logged out!")
    session.pop("user")
    return redirect(url_for("home"))


@app.route("/add-exercise", methods=["GET", "POST"])
def add_new_exercise():
    '''
    Will render add new exercise page, and show form to create
    a new exercise and post that data to the database. Also shows
    only the body targets available in the database.
    '''
    if request.method == "POST":
        exercise = {
            "body_target": request.form.get("body_target"),
            "exercise_name": request.form.get("exercise_name"),
            "instruction": request.form.get("instruction"),
            "est_time": request.form.get("est_time"),
            "difficulty": request.form.get("difficulty"),
            "user": session["user"]
        }
        mongo.db.exercises.insert_one(exercise)
        flash("Exercise sucessfully submitted to the database")
        return redirect(url_for("profile"))

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    category_name = mongo.db.target_category.find().sort("body_target", 1)
    return render_template("pages/add-exercise.html", username=username, category_name=category_name)


@app.route("/edit_exercise/<exercise_id>", methods=["GET", "POST"])
def edit_exercise(exercise_id):
    '''
    edit exercise
    '''
    if request.method == "POST":
        submit = {
            "body_target": request.form.get("body_target"),
            "exercise_name": request.form.get("exercise_name"),
            "instruction": request.form.get("instruction"),
            "est_time": request.form.get("est_time"),
            "difficulty": request.form.get("difficulty"),
            "user": session["user"]
        }
        mongo.db.exercises.update({"_id": ObjectId(exercise_id)}, submit)
        flash("Exercise updated successfully")
        return redirect(url_for("profile"))
    
    exercise = mongo.db.exercises.find_one({"_id": ObjectId(exercise_id)})
    category_name = mongo.db.exercises.find().sort("body_target", 1)
    return render_template("pages/edit-exercise.html", exercise=exercise, category_name=category_name)


@app.route("/delete/<exercise_id>")
def delete_exercise(exercise_id):
    '''
    will delete exercise from database and return user to 
    their profile page, with a flash message to confirm.
    '''
    mongo.db.exercises.remove({"_id": ObjectId(exercise_id)})
    flash("Exercise deleted.")
    return redirect(url_for("profile"))


@app.route("/workout_add/<exercise_id>")
def add_to_workout(exercise_id):
    '''
    will add exercise to users workout list
    by adding exercise _id to an array in user in database
    '''
    user = mongo.db.users
    current_user = user.find_one({ "user": session["user"].lower() })
    user.find_one_and_update(current_user, { "$push": {"workout": ObjectId(exercise_id)}})
    flash("Exercise added to your workout list.")
    return redirect(url_for("profile"))


@app.route("/contact")
def contact():
    '''
    renders a contact page, then on submission send email to developer
    via emailJS api
    '''
    return render_template("pages/contact.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
