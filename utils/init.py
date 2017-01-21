import sqlite3
import os

keyFile = open("data/key", "w")
keyFile.write(os.urandom(32))
keyFile.close()

f = "data/database.db"

db = sqlite3.connect(f)
c = db.cursor()

q = "CREATE TABLE users(username TEXT, password TEXT, email TEXT)"
c.execute(q)

q = "CREATE TABLE ious(note TEXT, amount INTEGER, dateCreated TEXT, dateModified TEXT, usernameLender TEXT, usernameBorrower TEXT, borrowOrLend TEXT, accountOrName TEXT, completed INTEGER, iouID INTEGER)"
c.execute(q)

db.commit()
db.close()
