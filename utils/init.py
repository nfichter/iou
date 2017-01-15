import sqlite3
import os

keyFile = open("data/key", "w")
keyFile.write(os.urandom(32))
keyFile.close()

f = "data/database.db"

db = sqlite3.connect(f)
c = db.cursor()

q = "CREATE TABLE users(username TEXT, password TEXT, email TEXT, userID INTEGER)"
c.execute(q)

q = "CREATE TABLE ious(note TEXT, amount INTEGER, dateCreated FLOAT, dateModified FLOAT, userIDLender INTEGER, userIDBorrower INTEGER, completed INTEGER)"
c.execute(q)

db.commit()
db.close()
