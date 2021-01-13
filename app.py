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


# landing page
@app.route("/home-loggedin")
def home_logged_in():
    '''
    This function loads the home landing page, displays all exercises,
    and will allow logged in users to see which ones are already in their 
    workout, and allow them to add / remove exercises.
    '''
    exercises = mongo.db.exercises.find()

    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    
    if username:
        current_user_obj = mongo.db.users.find_one({'username': session['user'].lower()})
        current_user_workout = current_user_obj['workout']
        workout_exercises = []
        workout_exercise_id = []

        if len(current_user_workout) != 0:
            for exercise in current_user_workout:
                current_exercise = mongo.db.exercises.find_one({'_id': exercise})
                current_exercise_id = current_exercise['_id']
                workout_exercise_id.append(current_exercise_id)
    
        for exercise in current_user_workout:
            current_exercise = mongo.db.exercises.find_one({'_id': exercise})
            workout_exercises.append(current_exercise)

        userexercises = mongo.db.exercises.find({ "user": username })
        return render_template("pages/home.html", username=username, exercises=exercises, userexercises=list(userexercises),
                                workout_exercise_id=workout_exercise_id, workout_exercises=workout_exercises)
    
    else:
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
            "password": generate_password_hash(request.form.get("password")),
            "workout": []
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
    
    current_user_obj = mongo.db.users.find_one({'username': session['user'].lower()})
    current_user_workout = current_user_obj['workout']
    workout_exercises = []
    workout_exercise_id = []

    if len(current_user_workout) != 0:
        for exercise in current_user_workout:
            current_exercise = mongo.db.exercises.find_one({'_id': exercise})
            current_exercise_id = current_exercise['_id']
            workout_exercise_id.append(current_exercise_id)
    
    for exercise in current_user_workout:
        current_exercise = mongo.db.exercises.find_one({'_id': exercise})
        workout_exercises.append(current_exercise)

    if username:
        userexercises = mongo.db.exercises.find({ "user": username })
        return render_template("pages/profile.html", username=username, userexercises=list(userexercises),
                                workout_exercise_id=workout_exercise_id, workout_exercises=workout_exercises)

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
        est_time_input = request.form.get("est_time")
        est_time = 9 if int(est_time_input) >= 9 else est_time_input

        exercise = {
            "body_target": request.form.get("body_target"),
            "exercise_name": request.form.get("exercise_name"),
            "instruction": request.form.get("instruction"),
            "est_time": est_time,
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
    also makes sure that, defensively, an est time is always a maximum of 9.
    '''
    if request.method == "POST":
        est_time_input = request.form.get("est_time")
        est_time = 9 if int(est_time_input) >= 9 else est_time_input

        submit = {
            "body_target": request.form.get("body_target"),
            "exercise_name": request.form.get("exercise_name"),
            "instruction": request.form.get("instruction"),
            "est_time": est_time,
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
    Will also remove itsself from any workout it might appear in.
    '''
    mongo.db.exercises.remove({"_id": ObjectId(exercise_id)})
# WORK FROM HERE
    users = mongo.db.users

    # for user in users:
    #     if exercise_id in user.workout[]:
    #         user.remove({"_id": ObjectId(exercise_id)})
    
    def search_work_out()


    flash("Exercise deleted.")
    return redirect(url_for("profile"))


@app.route("/workout")
def workout():
    '''
    renders workout page etc etc
    '''
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    current_user_obj = mongo.db.users.find_one({'username': session['user'].lower()})
    current_user_workout = current_user_obj['workout']
    workout_exercises = []
    workout_exercise_id = []

    if len(current_user_workout) != 0:
        for exercise in current_user_workout:
            current_exercise = mongo.db.exercises.find_one({'_id': exercise})
            current_exercise_id = current_exercise['_id']
            workout_exercise_id.append(current_exercise_id)
    
    for exercise in current_user_workout:
        current_exercise = mongo.db.exercises.find_one({'_id': exercise})
        workout_exercises.append(current_exercise)

    if username:
        userexercises = mongo.db.exercises.find({ "user": username })
        return render_template("pages/workout.html", username=username, userexercises=list(userexercises),
                                workout_exercise_id=workout_exercise_id, workout_exercises=workout_exercises)
    return render_template("pages/workout.html")


@app.route("/workout_add/<exercise_id>")
def add_to_workout(exercise_id):
    '''
    will add exercise to users workout list
    by adding exercise _id to an array in user in database
    '''
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$push": {"workout": ObjectId(exercise_id)}})
    flash("Exercise added to your workout list.")
    return redirect(url_for("workout"))


@app.route("/workout_remove/<exercise_id>")
def remove_from_workout(exercise_id):
    '''
    will remove exercise from workout by taking the 
    _id out of the users workout array in the database.
    '''
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$pull": {"workout": ObjectId(exercise_id)}})

    flash("Exercise removed from your workout")
    return redirect(url_for("workout"))


@app.route("/contact")
def contact():
    '''
    renders a contact page, then on submission send email to developer
    via emailJS api
    '''
    return render_template("pages/contact.html")


@app.errorhandler(404)
def not_found(error):
    '''
    Will catch 404 error for when a Page is not found and 
    render error page to display error to user with a redirect 
    to home.
    '''
    error_code = str(error)
    return render_template("pages/not_found.html", error_code=error_code), 404


@app.errorhandler(400)
def bad_request(error):
    '''
    Will catch 400 error for when a bad request occurs and 
    render error page to display error to user with a redirect 
    to home.
    '''
    error_code = str(error)
    return render_template("pages/not_found.html", error_code=error_code), 400


@app.errorhandler(500)
def server_error(error):
    '''
    Will catch 500 error for when an internal server error occurs and 
    render error page to display error to user with a redirect 
    to home.
    '''
    error_code = str(error)
    return render_template("pages/not_found.html", error_code=error_code), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
