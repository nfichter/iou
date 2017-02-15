from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
from utils import users
from utils import iou

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
	return render_template("register.html",message=message)

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

@app.route("/create", methods=["POST"])
def create():
	if not "username" in session:
		return redirect("/")
	note = request.form.get("note")
	amount = request.form.get("amount")
	if request.form.get("lendOrBorrow") == "lending":
		borrowOrLend = "lend"
		if request.form.get("otherAccount") == "yes": 
			accountOrName = "account"
			if users.get_user(request.form.get("accountName")) is not None:
				borrower = request.form.get("accountName")
				lender = session["username"]
			else:
				return redirect(url_for("new", messages="User does not exist."))
		else:
			accountOrName = "name"
			borrower = request.form.get("noAccountName")
			lender = session["username"]
	else:
		borrowOrLend = "borrow"
		if request.form.get("otherAccount") == "yes":
			accountOrName = "account"
			if users.get_user(request.form.get("accountName")) is not None:
				lender = users.get_user(request.form.get("accountName"))
				borrower = users.get_user(session["username"])
			else:
				return redirect(url_for("new", messages="User does not exist."))
		else:
			accountOrName = "name"
			lender = request.form.get("noAccountName")
			borrower = users.get_user(session["username"])
	iou.create(note,amount,lender,borrower,borrowOrLend,accountOrName)
	return redirect("/home") #redirect to newly created iou page once ready

@app.route("/home")
def home():
	if not "username" in session:
		return redirect("/")
	iouList = iou.getIOUs(session["username"])
	iouList.reverse()
	return render_template("home.html",iouList=iouList[:3],username=session["username"])

@app.route("/ious")
def ious():
	if not "username" in session:
		return redirect("/")
	iouList = iou.getIOUs(session["username"])
	iouListComplete = []
	for i in iouList:
		if str(i[8]) == "1":
			iouListComplete.append(i)
			iouList.remove(i)
	iouListComplete.reverse()
	iouList.reverse()
	return render_template("ious.html",iouList=iouList,iouListComplete=iouListComplete,username=session["username"])

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

@app.route("/modify/<int:iouId>")
def modify(iouId = None):
	iouInfo = iou.getIOU(iouId)
	print iouInfo
	return render_template("modify.html",info=iouInfo)
	
@app.route("/complete/<int:iouId>")
def complete(iouId = None):
	iouInfo = iou.getIOU(iouId)
	return render_template("complete.html",info=iouInfo)

@app.route("/modcom/<int:iouId>", methods=["POST"])
def modcom(iouId = None):
	if "modify" in request.form:
		iou.modify(iouId,request.form.get("amount"))
	if "complete" in request.form:
		iou.complete(iouId)
	return redirect("/ious")

@app.route("/logout")
def logout():
	if "username" in session:
		session.pop("username")
	return redirect("/")

if __name__ == "__main__":
	app.debug = True
	app.run()
