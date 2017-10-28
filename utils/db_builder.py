import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


#==========================================================
'''
TABLE CREATION
Database usersandstories.db
Tables: users, stories, updates
'''

def tableCreation():
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #Create the users table
    user_table = 'CREATE TABLE users (username TEXT, password BLOB, userID INTEGER);'
    c.execute(user_table)
    #Create the stories table
    stories_table = 'CREATE TABLE stories (storyID INTEGER, title TEXT, author INTEGER, content TEXT);'
    c.execute(stories_table)
    #Create the updates table
    update_table = 'CREATE TABLE updates (storyID INTEGER, contribution TEXT, contributor INTEGER);'
    c.execute(update_table)
    db.commit()
    db.close()

#==========================================================

#COUNTERS
userID_counter = 0;  #helps to assign userID
storyID_counter = 0; #helps to assign storyID

#==========================================================

#ADD VALUES TO TABLES

#add a user
def addUser(new_username, new_password):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    global userID_counter
    new_userID = userID_counter
    userID_counter += 1
    c.execute('INSERT INTO users VALUES (?,?,?)',[new_username, new_password, new_userID])
    db.commit()
    db.close()


#add a new story
def addStory(new_title, st_author, st_content):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    global storyID_counter
    storyID_counter += 1
    new_storyID = storyID_counter
    c.execute('INSERT INTO stories VALUES (?,?,?,?)',[new_storyID, new_title, st_author, st_content])
    c.execute('INSERT INTO updates VALUES (?,?,?)',[new_storyID, st_content, st_author])
    db.commit()
    db.close()


#make an update to a story
def addUpdate(new_storyID, new_content, new_contributor):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    c.execute('INSERT INTO updates VALUES (?,?,?)',[new_storyID, new_content, new_contributor])
    c.execute('SELECT content FROM stories WHERE storyID= ' + str(new_storyID) + ';')
    old_content = c.fetchone()
    #print 'OLD CONTENT...'
    #print old_content
    final_content = old_content[0] +' ' + new_content
    #print 'NEW CONTENT...'
    #print final_content
    c.execute('UPDATE stories SET content ="' + final_content + '" WHERE storyID =' + str(new_storyID) + ';')
    db.commit()
    db.close()

def getLastEdit(st_ID):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    all_edits = c.execute('SELECT contribution FROM updates WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in all_edits:
        retVal = x[0]
    db.close()
    return retVal

def getFullStory(st_ID):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    story = c.execute('SELECT content FROM stories WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in story:
        retVal = x[0]
    db.close()
    return retVal

def getTitle(st_ID):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    retTitle = c.execute('SELECT title FROM stories WHERE storyID= ' + str(st_ID) + ';')
    retVal = ''
    for x in retTitle:
        retVal =  x[0]
    db.close()
    return retVal

def checkUsername(userN):
    f="usersandstories.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    users = c.execute('SELECT username FROM users;')
    result = False
    for x in users:
        if (x[0] == userN):
            result = True
    db.close()
    return result

#==========================================================
#ACCESSORS
def getPass(username):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM users"
    info = c.execute(command)

    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal

def getUserID(username):
    f="usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, userID FROM users"
    info = c.execute(command)

    retVal = None
    for user in info:
        if str(user[0]) == username:
            retVal = str(user[1])
    db.close()
    return retVal

#==========================================================
#HELPERS
def hasContributed(thisUser,thisStory):
    f="usersandstories.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    con = c.execute('SELECT contributor FROM updates WHERE storyID = ' + str(thisStory) + ';')
    
    for row in con:
        if row[0]==thisUser:
            db.close()
            return True
        #print row[0]
    db.close()

if __name__ == '__main__':     
    #TESTING
    tableCreation()
    
    #add users
    addUser('manahal', 'mt123')
    addUser('joe', 'fgh349')
    addUser('bob', 'iryg9137')
    addUser('sasha', 'jfhv173')
    
    #make story
    addStory('welcome', 0, 'well hello there')
    addStory('bye', 3, 'we enjoyed the time')
    
    #update story
    addUpdate(0, 'how are you doing', 1)
    addUpdate(1, 'we will see you later', 3)
    addUpdate(0, 'doing fine', 2)
    addUpdate(1, 'kk will do', 0)
    
    #get the last edit
    getLastEdit(0)
    getLastEdit(1)
    
    #get full story
    print getFullStory(0)
    print getFullStory(1)
    
    #get title
    print getTitle(0)
    print getTitle(1)
    
    #check if somebody's edited the story
    print "Has user 1 edited story 0 (should be True): " + str( hasContributed(1,0) )
    print "Has user 6 edited story 0 (should be False): " + str( hasContributed(6,0) )
    print "Has user 3 edited story 0 (should be False): " + str( hasContributed(3,0) )
    print "Has user 2 edited story 0 (should be True): " + str( hasContributed(2,0) )
