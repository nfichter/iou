from hashlib import sha1
import sqlite3

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

	c.execute("SELECT MAX(userID) FROM users")
	res = c.fetchone()

	max_id = res[0]
	
	if max_id == None:
		userid = 0
	else:
		userid = max_id + 1

	passHash = sha1(password).hexdigest()
	c.execute("INSERT INTO users VALUES('%s','%s','%s','%s')" %(username,email,passHash,userid))

	db.commit()
	db.close()

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
		user["id"] = res[3]
		
		return user
		
def get_user_by_id(userID):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM users WHERE userID=='%s'" %(userID))
	res = c.fetchone()
	
	if res == None:
		return None
	else:
		user = {}
		user["username"] = username
		user["email"] = res[2]
		user["id"] = res[3]
		
		return user