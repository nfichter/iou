import sqlite3
import datetime

#returns iouID
def create(note,amount,dateCreated,userIDLender,userIDBorrower):
	f = "data/database.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    
    c.execute("SELECT MAX(userID) FROM users")
    res = c.fetchone()

    max_id = res[3]
    
    if max_id == None:
        iouID = 0
    else:
        iouID = max_id + 1
        
    currentTime = datetime.datetime.utcfromtimestamp(0)
        
    c.execute("INSERT INTO ious VALUES('%s','%s','%s','%s')" %(note,amount,currentTime,currentTime,userIDLender,userIDBorrower,0,iouID))

    db.commit()
    db.close()
    
    return iouID

#returns 0 if successful, -1 if iou with ID iouID does not exist
def modify(iouID,amountPaid,dateModified):
	f = "data/database.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    
    c.execute("SELECT * FROM ious WHERE iouID == '%s'",%(iouID))
    res = c.fetchone()
    
    if res == None:
    	return -1
    
    dateModified = datetime.datetime.utcfromtimestamp(0)
    amount = int(res[1])-amountPaid
    
    c.execute("UPDATE ious SET amount='%s' where iouID='%s'"%(amount,iouID))
    c.execute("UPDATE ious SET dateModified='%s' where iouID='%s'"%(dateModified,iouID))
    
    db.commit()
    db.close()