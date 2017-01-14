from flask import Flask, render_template, request, session, redirect, url_for
import hashlib

app = Flask(__name__)
app.secret_key = "asdf"

@app.route("/")
def landing():
    if "username" in session:
        return redirect("/home")
    return render_template("landing.html")

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
