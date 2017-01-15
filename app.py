from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
from utils import users

app = Flask(__name__)
app.secret_key = "asdf"

@app.route("/")
def landing():
    if "username" in session:
        return redirect("/home")
    return render_template("landing.html")

@app.route("/register")
def register():
    message = ""
    if "messages" in request.args:
        if request.args["messages"] == "0":
            message = "Passwords don't match."
        if request.args["messages"] == "1":
            message = "Emails don't match."
        if request.args["messages"] == "2":
            message = "Username is taken."
    return render_template("register.html",message = message)

@app.route("/login")
def login():
    message = ""
    if "messages" in request.args:
        if request.args["messages"] == "0":
            message = "Username doesn't exist."
        if request.args["messages"] == "1":
            message = "Incorrect password."
    return render_template("login.html", message = message)

@app.route("/auth", methods=["POST"])
def auth():
    if "login" in request.form:
        username = request.form.get("user")
        password = request.form.get("pass")
        ret = users.login(username,password)
        if ret == 0 or ret == 1:
            return redirect(url_for("login", messages=str(ret)))
        else:
            session["username"] = username
            return redirect("/home")
    elif "register" in request.form:
        username = request.form.get("user")
        password = request.form.get("pass")
        passConf = request.form.get("passConf")
        email = request.form.get("email")
        emailConf = request.form.get("emailConf")
        ret = users.register(username,password,passConf,email,emailConf)
        if ret == 0 or ret == 1 or ret == 2:
            return redirect(url_for("register", messages=str(ret)))
        else:
            return redirect("/login")
    else:
        return redirect("/")

@app.route("/home")
def home():
    if not "username" in session:
        return redirect("/")
    return render_template("home.html")

@app.route("/new")
def new():
    if not "username" in session:
        return redirect("/")
    return render_template("new.html")

@app.route("/profile")
def profile():
    if not "username" in session:
        return redirect("/")
    return render_template("profile.html")

@app.route("/settings")
def settings():
    if not "username" in session:
        return redirect("/")
    return render_template("settings.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
