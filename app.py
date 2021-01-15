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


# home page not logged in
@app.route("/")
def home():
    """
    This function loads the home landing page. Gets all exercises 
    from the database and sends them to the page to iterate over,
    using variable exercises.
    """
    exercises = mongo.db.exercises.find()
    
    return render_template("pages/home.html", exercises=exercises)   


# home page logged in
@app.route("/home-loggedin")
def home_logged_in():
    """
    This function loads the home landing page, checks if there is a user logged in
    then finds that users' workout array.
    It checks if that array is empty or not, if it isn't empty, then it goes through
    that array and populates the workout_exercises list to be passed to the page.
    It also passes all the exercises to the page to iterate over, too.
    These variables allow the page to show wether an exercise was made by
    the logged in user or not, and show edit/delete options if so.
    """
    exercises = mongo.db.exercises.find()

    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    
    if username:
        current_user_obj = mongo.db.users.find_one({'username': session['user'].lower()})
        current_user_workout = current_user_obj['workout']
        workout_exercises = []
        workout_exercise_id = []

        if len(current_user_workout) != 0:
            for exercise in current_user_workout:
                current_exercise = mongo.db.exercises.find_one({'_id': ObjectId(exercise)})
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
    """
    Will render register page and handle account register on POST.
    This posts user details into database and check to see if 
    user already exists - if username already exists it flashes
    a message for the user to try and log in or try another username.
    On password submission, hashes password using Werkeug.
    """
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
    """
    Will render log in page and create session cookie for user session.
    Also checks for if password matches with database, with messages for if incorrect.
    """
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
    """
    Will render profile page and create variables for page to use.
    Username is passed for header text and to check through the 
    user exercises list for matches so as to send only the users exercises to page.
    Will also check against the users workout array for matches, so the page can 
    correctly show what exercies are already in the users workout list.
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    current_user_obj = mongo.db.users.find_one({'username': session['user'].lower()})
    current_user_workout = current_user_obj['workout']
    workout_exercises = []
    workout_exercise_id = []

    if current_user_workout != []:
        for exercise in current_user_workout:
            current_exercise = mongo.db.exercises.find_one({'_id': ObjectId(exercise)})
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
    """
    Will pop user session cookie out of memory, and return to
    non-logged in home page.
    """
    flash("You have been successfully logged out!")
    session.pop("user")
    return redirect(url_for("home"))


@app.route("/add-exercise", methods=["GET", "POST"])
def add_new_exercise():
    """
    Will render add new exercise page, and show form to create
    a new exercise and post that data to the database. Also shows
    only the body targets available in the database.
    Some defensive paramters also included for if user changes html, such as
    estimate time max value and title and instruction length.
    """
    if request.method == "POST":
        exercise_name_input = request.form.get("exercise_name")
        if len(exercise_name_input) >= 21:
            flash("Title is too long, max = 20 characters")
            return redirect(url_for("add_new_exercise"))
        
        exercise_instruction_input = request.form.get("instruction")
        if len(exercise_instruction_input) >= 91:
            flash("Intstruction is too long, max = 90 characters")
            return redirect(url_for("add_new_exercise"))

        est_time_input = request.form.get("est_time")
        est_time = 9 if int(est_time_input) >= 9 else est_time_input

        exercise = {
            "body_target": request.form.get("body_target"),
            "exercise_name": exercise_name_input,
            "instruction": exercise_instruction_input,
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
    """
    Will render edit exercise page, and show form to pre-populated with
    current exercise.
    Will post any data in form to the database, overwriting what was previously there.
    Also shows only the body targets available in the database.
    Some defensive paramters also included for if user changes html, such as
    estimate time max value and title and instruction length.
    """
    if request.method == "POST":
        exercise_name_input = request.form.get("exercise_name")
        if len(exercise_name_input) >= 21:
            flash("Title is too long, max = 20 characters")
            return redirect(url_for("add_new_exercise"))
        
        exercise_instruction_input = request.form.get("instruction")
        if len(exercise_instruction_input) >= 91:
            flash("Intstruction is too long, max = 90 characters")
            return redirect(url_for("add_new_exercise"))

        est_time_input = request.form.get("est_time")
        est_time = 9 if int(est_time_input) >= 9 else est_time_input

        submit = {
            "body_target": request.form.get("body_target"),
            "exercise_name": exercise_name_input,
            "instruction": exercise_instruction_input,
            "est_time": est_time,
            "difficulty": request.form.get("difficulty"),
            "user": session["user"]
        }
        mongo.db.exercises.update({"_id": ObjectId(exercise_id)}, submit)
        flash("Exercise updated successfully")
        return redirect(url_for("profile"))
    
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    exercise = mongo.db.exercises.find_one({"_id": ObjectId(exercise_id)})
    category_name = mongo.db.target_category.find().sort("body_target", 1)
    return render_template("pages/edit-exercise.html", username=username, exercise=exercise, category_name=category_name)


@app.route("/delete/<exercise_id>")
def delete_exercise(exercise_id):
    """
    Will delete exercise from database and return user to 
    their profile page, with a flash message to confirm using
    exercise id to cross check correct exercise being deleted.
    Also checks if the current exercise is in any users workout and
    removes from their workout also to avoid loading errors for other users.
    """
    users = mongo.db.users.find()

    for user in list(users):
        if exercise_id in user['workout']:
            mongo.db.users.update({"_id": ObjectId(user['_id'])}, {"$pull": {"workout": exercise_id}})

    mongo.db.exercises.remove({"_id": ObjectId(exercise_id)})

    flash("Exercise deleted.")
    return redirect(url_for("profile"))


@app.route("/workout")
def workout():
    """
    Will render workout page, checking user workout array against the 
    exercise collection to show the correct data.
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    current_user_obj = mongo.db.users.find_one({'username': session['user'].lower()})
    current_user_workout = current_user_obj['workout']
    workout_exercises = []
    workout_exercise_id = []

    if len(current_user_workout) != 0:
        for exercise in current_user_workout:
            current_exercise = mongo.db.exercises.find_one({'_id': ObjectId(exercise)})
            current_exercise_id = current_exercise['_id']
            workout_exercise_id.append(current_exercise_id)
    
    for exercise in current_user_workout:
        current_exercise = mongo.db.exercises.find_one({'_id': ObjectId(exercise)})
        workout_exercises.append(current_exercise)

    if username:
        userexercises = mongo.db.exercises.find({ "user": username })
        return render_template("pages/workout.html", username=username, userexercises=list(userexercises),
                                workout_exercise_id=workout_exercise_id, workout_exercises=workout_exercises)
    return render_template("pages/workout.html")


@app.route("/workout_add/<exercise_id>")
def add_to_workout(exercise_id):
    """
    Adds exercise to users workout list by pushing 
    exercise _id string to a workout array in user in database.
    """
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$push": {"workout": exercise_id}})
    flash("Exercise added to your workout list.")
    return redirect(url_for("workout"))


@app.route("/workout_remove/<exercise_id>")
def remove_from_workout(exercise_id):
    """
    Removes exercise from workout by taking the id string 
    out of the users workout array in the database.
    """
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$pull": {"workout": exercise_id}})

    flash("Exercise removed from your workout")
    return redirect(url_for("workout"))


@app.route("/contact")
def contact():
    """
    Renders the contact page.
    """
    return render_template("pages/contact.html")


@app.errorhandler(404)
def not_found(error):
    """
    Will catch 404 error for when a Page is not found and 
    render error page to display error to user with a redirect 
    to home.
    """
    error_code = str(error)
    return render_template("pages/not-found.html", error_code=error_code), 404


@app.errorhandler(400)
def bad_request(error):
    """
    Will catch 400 error for when a bad request occurs and 
    render error page to display error to user with a redirect 
    to home.
    """
    error_code = str(error)
    return render_template("pages/not-found.html", error_code=error_code), 400


@app.errorhandler(500)
def server_error(error):
    """
    Will catch 500 error for when an internal server error occurs and 
    render error page to display error to user with a redirect 
    to home.
    """
    error_code = str(error)
    return render_template("pages/not-found.html", error_code=error_code), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
