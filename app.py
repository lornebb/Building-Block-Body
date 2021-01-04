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
def log_in_register():
    '''
    Will render log in and register page and handle either log in or account register 
    and post user details into database or check to see if user already exists.
    '''
    if request.method == "POST":
        existing_user = mongo.db.exercises.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists, please try another one")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Success! You are now registered")
    return render_template("login_and_register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
