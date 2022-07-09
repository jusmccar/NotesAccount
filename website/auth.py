from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if valid_signup(email, first_name, password1, password2):
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if valid_login(user, password):
            login_user(user, remember=True)
            flash("Logged in!", category="success")
            return redirect(url_for("views.home"))

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

def valid_signup(email, first_name, password1, password2):
    EMAIL_LEN = 4
    FIRST_NAME_LEN = 2
    PASSWORD_LEN = 7
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Account already exists with specified email.", category="error")
        return False
    elif len(email) < EMAIL_LEN:
        flash(f"Email must be at least {EMAIL_LEN} characters.", category="error")
        return False
    elif len(first_name) < FIRST_NAME_LEN:
        flash(f"First name must be at least {FIRST_NAME_LEN} characters.", category="error")
        return False
    elif len(password1) < PASSWORD_LEN:
        flash(f"Password must be at least {PASSWORD_LEN} characters.", category="error")
        return False
    elif password1 != password2:
        flash("Passwords must match.", category="error")
        return False

    return True

def valid_login(user, password):
    if user:
        if check_password_hash(user.password, password):
            return True
        else:
            flash("Incorrect password, try again.", category="error")
    else:
        flash("No account exists with specified email.", category="error")

    return False
