import sqlite3
import datetime

#returns iouID
def create(note,amount,userIDLender,userIDBorrower,borrowOrLend,accountOrName):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT MAX(userID) FROM users")
	res = c.fetchone()
	max_id = res[0]
	
	if max_id == None:
		iouID = 0
	else:
		iouID = max_id + 1
		
	currentTime = datetime.datetime.utcfromtimestamp(0)
		
	c.execute("INSERT INTO ious VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(note,amount,currentTime,currentTime,userIDLender,userIDBorrower,borrowOrLend,accountOrName,0,iouID))

	db.commit()
	db.close()
	
	return iouID

#returns 0 if successful, None if iou with ID iouID does not exist
def modify(iouID,amountPaid,dateModified):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM ious WHERE iouID == '%s'"%(iouID))
	res = c.fetchone()
	
	if res == None:
		return None
	
	dateModified = datetime.datetime.utcfromtimestamp(0)
	amount = int(res[1])-amountPaid
	
	c.execute("UPDATE ious SET amount='%s' where iouID='%s'"%(amount,iouID))
	c.execute("UPDATE ious SET dateModified='%s' where iouID='%s'"%(dateModified,iouID))
	
	db.commit()
	db.close()
	
#returns a list of all of a user's IOUs, None if the user has no IOUs
def getIOUs(userID):
	f = "data/database.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	
	c.execute("SELECT * FROM ious WHERE userIDLender='%s' OR userIDBorrower='%s'" %(userID,userID))
	res = c.fetchall()
	
	if res == None:
		return None
	
	ret = []
	for line in res:
		ret.append(line)
		
	return ret