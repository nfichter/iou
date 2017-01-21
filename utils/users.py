from hashlib import sha1
import sqlite3
import smtplib

#sends an email from the no-reply account
def send_mail(subject, body, email):
	smtpObj = smtplib.SMTP("smtp.gmail.com",587)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login('noreply.ioweu@gmail.com','PASS_GOES_HERE')
	smtpObj.sendmail('noreply.ioweu@gmail.com',email,'Subject: %s\n%s'%(subject,body))

#returns 0 if passwords don't match, 1 if emails don't match, 2 if username is taken, 3 if successful
def register(username, password, passwordMatch, email, emailMatch):
	if password != passwordMatch:
		return 0

	if email != emailMatch:
		return 1
	
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()

	c.execute("SELECT * FROM users WHERE username == '%s'" %username)
	res = c.fetchone()

	if res != None:
		return 2

	passHash = sha1(password).hexdigest()
	c.execute("INSERT INTO users VALUES('%s','%s','%s')" %(username,email,passHash))

	db.commit()
	db.close()

	send_mail("Welcome to IOweU!","Hey %s! Welcome to IOweU.\nFeel free to email ioweyouapp.custserv@gmail.com if you have any questions."%(username),email)

	return 3

#returns 0 if username doesn't exist, 1 if incorrect password, 2 if successful
def login(username, password):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()

	c.execute("SELECT * FROM users WHERE username=='%s'" %(username))
	res = c.fetchone()

	db.commit()
	db.close()
	
	if res == None:
		return 0
	if res[2] == sha1(password).hexdigest():
		return 2
	else:
		return 1

#returns None if user doesn't exist, dictionary with username, email, user id if user exists
def get_user(username):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM users WHERE username=='%s'" %(username))
	res = c.fetchone()
	
	if res == None:
		return None
	else:
		user = {}
		user["username"] = username
		user["email"] = res[2]
		
		return user