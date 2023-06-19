import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        correctDate = None

        name = request.form.get("name")
        month = 0
        day = 0
        try:
            month = int(request.form.get("month"))
            day = int(request.form.get("day"))
            datetime.datetime(year=2020, month=month, day=day)
            correctDate = True
        except:
            correctDate = False

        if correctDate:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        people = db.execute("SELECT * FROM birthdays;")

        return render_template("index.html", people=people)


@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    id = request.form.get("id")
    newname = request.form.get("newname")
    newmonth = request.form.get("newmonth")
    newday = request.form.get("newday")
    if id and newmonth and newday:
        db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?;", newname, newmonth, newday, id)

    return redirect("/")