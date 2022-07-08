from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        valid_signup(email, first_name, password1, password2)

    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return render_template("home.html")

def valid_signup(email, first_name, password1, password2):
    EMAIL_LEN = 4
    FIRST_NAME_LEN = 2
    PASSWORD_LEN = 7

    if len(email) < EMAIL_LEN:
        flash("Email must be at least " + str(EMAIL_LEN) + " characters.", category="error")
        return False
    elif len(first_name) < FIRST_NAME_LEN:
        flash("First name must be at least " + str(FIRST_NAME_LEN) + " characters.", category="error")
        return False
    elif len(password1) < PASSWORD_LEN:
        flash("Password must be at least " + str(PASSWORD_LEN) + " characters.", category="error")
        return False
    elif password1 != password2:
        flash("Passwords must match.", category="error")
        return False

    flash("Account created!", category="success")
    return True
