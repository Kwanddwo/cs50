import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from re import search

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM (SELECT symbol, shares FROM purchases WHERE user_id = ?) GROUP BY symbol;", session["user_id"])
    if not portfolio:
        portfolio = db.execute("SELECT symbol, SUM(shares) AS shares FROM purchases WHERE user_id = ?;", session["user_id"])

    balancedb = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    balance = balancedb[0]["cash"]

    if portfolio:
        try:
            stocks_total_value = 0
            for stock in portfolio:
                lookedup = lookup(stock["symbol"])
                stocks_total_value += lookedup["price"] * stock["shares"]
                stock["holding"] = lookedup["price"] * stock["shares"]
                stock["price"] = lookedup["price"]
                stock["name"] = lookedup["name"]
        except:
            return render_template("index.html")

        grandtotal = balance + stocks_total_value

        return render_template("index.html", portfolio=portfolio, balance=balance, grandtotal=grandtotal)

    return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    balancedb = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    balance = balancedb[0]["cash"]

    if request.method == "POST":
        form_symbol = request.form.get("symbol")
        quote = lookup(form_symbol.upper())

        if not quote:
            return apology("Symbol not found")

        try:
            num_shares = int(request.form.get("shares"))
        except:
            return apology("Please input a positive number of shares")

        if num_shares < 1:
            return apology("Please input a positive number of shares")

        price = quote["price"] * num_shares

        if balance < price:
            return apology("Not enough cash")

        balance -= price

        db.execute("UPDATE users SET cash = ? WHERE id = ?;", balance, session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, DATETIME());",
                   session["user_id"], quote["symbol"], num_shares, quote["price"])

        flash(f"{num_shares} share(s) of {form_symbol.upper()} bought successfuly!")

        return redirect("/")

    return render_template("buy.html", balance=balance)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM purchases WHERE user_id = ? ORDER BY date DESC", session["user_id"])

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash succesful login
        flash("You have successfuly logged in")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("Incorrect symbol")

        return render_template("quote.html", quote=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        namesdb = db.execute("SELECT username FROM users")

        if not username or len(username) < 6:
            return apology("invalid username")

        if not password:
            return apology("invalid password")

        if not search("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}", password):
            return apology("invalid password format, must contain atleast one digit, one uppercase letter and one lowercase letter")

        if not confirm or password != confirm:
            return apology("invalid confirmaton")

        for i in range(len(namesdb)):
            if username == namesdb[i]["username"]:
                return apology("Name already in use")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        flash("You have been registered successfuly!")

        return render_template("login.html")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM (SELECT symbol, shares FROM purchases WHERE user_id = ?) GROUP BY symbol;", session["user_id"])
    if not portfolio:
        portfolio = db.execute("SELECT symbol, SUM(shares) AS shares FROM purchases WHERE user_id = ?;", session["user_id"])

    if request.method == "POST":
        selected_symbol = request.form.get("symbol")

        try:
            sold_shares = int(request.form.get("shares"))
        except:
            return apology("Incorrect number of shares")

        if sold_shares < 1:
            return apology("incorrect number of shares")

        for stock in portfolio:
            if selected_symbol == stock["symbol"]:
                lookedup = lookup(selected_symbol)

                if sold_shares > stock["shares"]:
                    return apology("Not enough shares")

                db.execute("INSERT INTO purchases (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, DATETIME());",
                           session["user_id"], selected_symbol, -sold_shares, lookedup["price"])

                balancedb = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
                balance = balancedb[0]["cash"]

                db.execute("UPDATE users SET cash = ? WHERE id = ?;", balance +
                           (sold_shares * lookedup["price"]), session["user_id"])

                flash(f"{sold_shares} share(s) of {selected_symbol} sold!")

                return redirect("/")

        return apology("You don't have shares in this stock!")

    return render_template("sell.html", portfolio=portfolio)

