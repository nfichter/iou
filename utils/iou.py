import sqlite3
import time
from utils import users

#returns iouID
def create(note,amount,usernameLender,usernameBorrower,borrowOrLend,accountOrName):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT MAX(iouID) FROM ious")
	res = c.fetchone()
	max_id = res[0]
	
	print max_id
	
	if max_id == None:
		iouID = 0
	else:
		iouID = max_id + 1
		
	currentTime = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(time.time()))
		
	c.execute("INSERT INTO ious VALUES(?,?,?,?,?,?,?,?,?,?)",(note,amount,currentTime,currentTime,usernameLender,usernameBorrower,borrowOrLend,accountOrName,0,iouID))

	db.commit()
	db.close()
	
	return iouID

#returns 0 if successful, None if iou with ID iouID does not exist
def modify(iouID,amountPaid):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM ious WHERE iouID == '%s'"%(iouID))
	res = c.fetchone()
	
	if res == None:
		return None
	
	dateModified = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(time.time()))
	amount = int(res[1])-amountPaid
	
	c.execute("UPDATE ious SET amount='%s' where iouID='%s'"%(amount,iouID))
	c.execute("UPDATE ious SET dateModified='%s' where iouID='%s'"%(dateModified,iouID))
	
	db.commit()
	db.close()

#returns 0 if successful, None if iou with ID iouID does not exist
def complete(iouID):
	
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM ious WHERE iouID == '%s'"%(iouID))
	res = c.fetchone()
	
	if res == None:
		return None
	
	dateModified = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(time.time()))
	amount = 0
	
	c.execute("UPDATE ious SET amount='%s' where iouID='%s'"%(amount,iouID))
	c.execute("UPDATE ious SET dateModified='%s' where iouID='%s'"%(dateModified,iouID))
	c.execute("UPDATE ious SET completed='1' where iouID='%s'"%iouID)
	
	db.commit()
	db.close()
	
#returns a dictionary of an IOU's properties
def getIOU(iouID):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM ious WHERE iouID='%s'" %(iouID))
	
	res = c.fetchall()
	
	ret = {}
	for line in res:
		ret["note"] = line[0]
		ret["amount"] = line[1]
		ret["dateCreated"] = line[2]
		ret["dateModified"] = line[3]
		ret["usernameLender"] = line[4]
		ret["usernameBorrower"] = line[5]
		ret["borrowOrLend"] = line[6]
		ret["accountOrName"] = line[7]
		ret["completed"] = line[8]
		ret["iouID"] = line[9]
		
	return ret
	
#returns a list of all of a user's IOUs, [] if the user has no IOUs
def getIOUs(username):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM ious WHERE usernameLender='%s' OR usernameBorrower='%s'" %(username,username))
	res = c.fetchall()
	
	ret = []
	i = 0
	for line in res:
		ret.append(line)
		
	return ret