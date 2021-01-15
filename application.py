import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
# for a list of error codes go to https://www.restapitutorial.com/httpstatuscodes.html

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filters
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///goals.db")


@app.route("/")
@login_required
def index():

    # store the user information logged in the session
    username = db.execute("SELECT username FROM users WHERE id=:uid", uid=int(session["user_id"]))[0]["username"]

    goals= db.execute("SELECT * FROM goals WHERE username = :username" , username=username)


    return render_template("index.html", goals = goals, username=username)

@app.route("/")
@login_required
def list_goals():

    # store the user information logged in the session
    username = db.execute("SELECT username FROM users WHERE id=:uid", uid=int(session["user_id"]))[0]["username"]
    print(username)
    goals= db.execute("SELECT * FROM goals WHERE username = :username" , username=username)

    return render_template("index.html", goals = goals)

@app.route("/set_goals",methods=["GET", "POST"])
@login_required
def set_goals():
    """(buy) request goals and adds them to the database """

    username = db.execute("SELECT username FROM users WHERE id=:uid", uid=int(session["user_id"]))[0]["username"]
    print(username)
    if request.method == "POST":
        # check that there is an entry
        if not request.form.get("goal_name") :
            return apology("goal cannot be empty", 406)

        goal_name = request.form.get("goal_name")
        goal_notes = request.form.get("goal_notes")
        db.execute("INSERT INTO goals (username, goal_name, goal_notes) VALUES( :username,:goal_name, :goal_notes)",
            username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"],
            goal_name=goal_name, goal_notes = goal_notes)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("set_goals.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        #  ensure confirmation password was submitted and matches password
        elif not request.form.get("confirmation") or not request.form.get("confirmation") == request.form.get("password"):
            return apology("password do not match", 400)

        # Query database for username and check if already exists
        duplicate = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(duplicate) != 0:
            return apology("username already exists", 400)


        # Store the information to the database

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                    username=request.form.get("username"),
                    hash=generate_password_hash(request.form.get("password")))

        # star the session
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]
        print(session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/completed_goal", methods=["GET", "POST"])
@login_required
def completed_goal():
    """mark goal completed"""

    username = db.execute("SELECT username FROM users WHERE id=:uid", uid=int(session["user_id"]))[0]["username"]
    print("1")
    print(username)

    if request.method =="POST":
        # check that there is an entry
        if not request.form.get("goal_name") :
            return apology("choose a goal to mark completed")

        goal_name = request.form.get("goal_name")
        status = request.form.get("status")
        print(goal_name)
        print(status)

        if request.form.get("status") == 'yes':
            db.execute("UPDATE goals SET done='true' WHERE username= :username AND goal_name= :goal_name",
                    username=username , goal_name = goal_name)

        # Send user to the main goal page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # get goals
        goals = db.execute("SELECT goal_name FROM goals WHERE username = :username", username=username)
        return render_template("completed_goal.html", goals= goals)

@app.route("/erase_goal", methods=["GET", "POST"])
@login_required
def erase_goal():
    """erase goal"""
    username = db.execute("SELECT username FROM users WHERE id=:uid", uid=int(session["user_id"]))[0]["username"]
    print(username)

    if request.method =="POST":
        # check that there is an entry
        if not request.form.get("goal_name") :
            return apology("choose a goal to erase")

        goal_name = request.form.get("goal_name")
        confirm = request.form.get("confirm")

        if request.form.get("confirm") == 'yes':
            db.execute("DELETE FROM goals WHERE username= :username AND goal_name= :goal_name",
                    username=username , goal_name = goal_name)

        # Send them to the main goal page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # get goals
        goals = db.execute("SELECT goal_name FROM goals WHERE username = :username", username=username)
        return render_template("erase_goal.html", goals= goals)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

"""
tables

CREATE TABLE 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
'username' TEXT NOT NULL,
'hash' TEXT NOT NULL );

CREATE TABLE 'goals' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
'username' TEXT FOREIG KEY,
'goal_name' TEXT NOT NULL,
'goal_notes' TEXT,
'goal_steps' TEXT,
'done' BOOLEAN NOT NULL DEFAULT false,
'time' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(username) REFERENCES users(username));

CREATE UNIQUE INDEX 'username' ON "users" ("username");

"""
